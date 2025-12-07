from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime
from typing import Optional, Dict, List
from config import Config

class DatabaseManager:
    """Manages MongoDB connections and operations"""
    
    def __init__(self):
        
        self.client = None
        self.db = None
        self.conversations = None
        self.connect()
    
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            print(f"🔄 Connecting to MongoDB...")
            print(f"   URI: {Config.MONGODB_URI[:20]}...")
            print(f"   Database: {Config.MONGODB_DATABASE}")
            
            self.client = MongoClient(
                Config.MONGODB_URI,
                serverSelectionTimeoutMS=10000
            )
            # Test connection
            self.client.admin.command('ping')
            
            self.db = self.client[Config.MONGODB_DATABASE]
            self.conversations = self.db[Config.CONVERSATIONS_COLLECTION]
            
            # Create indexes for better performance
            self._create_indexes()
            
            print(f"✅ Connected to MongoDB Cloud: {Config.MONGODB_DATABASE}")
            return True
            
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            print("💡 Please check your MongoDB Atlas connection string and network access")
            self.conversations = None
            return False
        except Exception as e:
            print(f"❌ Unexpected error connecting to MongoDB: {e}")
            print(f"   Error type: {type(e).__name__}")
            self.conversations = None
            return False
    
    def _create_indexes(self):
        """Create indexes for efficient querying"""
        # Index on created_at for time-based queries
        self.conversations.create_index("created_at")
        self.conversations.create_index("user_id")
    
    def save_complete_conversation(self,
                                   user_id: str,
                                   messages: List[Dict],
                                   conversation_summary: Dict,
                                   created_at: datetime) -> str:
        """
        Save complete conversation with all messages and overall sentiment
        
        Args:
            user_id: User identifier
            messages: List of all message exchanges
            conversation_summary: Overall sentiment and summary
            created_at: When conversation started
        
        Returns:
            conversation_id: The ID of the saved conversation
        """
        if self.conversations is None:
            raise ConnectionError("Not connected to MongoDB. Please check your connection.")
        
        conversation = {
            "user_id": user_id,
            "created_at": created_at,
            "completed_at": datetime.utcnow(),
            "total_messages": len(messages),
            "messages": messages,  # Full conversation history
            "overall_sentiment": conversation_summary.get("full_conversation_sentiment", {}),
            "sentiment_journey": conversation_summary.get("sentiment_journey", {}),
            "key_emotional_moments": conversation_summary.get("key_emotional_moments", []),
            "insights": conversation_summary.get("insights", []),
            "full_summary": conversation_summary  # Complete summary
        }
        
        result = self.conversations.insert_one(conversation)
        print(f"💾 Complete conversation saved to MongoDB (ID: {result.inserted_id})")
        return str(result.inserted_id)
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Get a conversation by ID"""
        from bson.objectid import ObjectId
        return self.conversations.find_one({"_id": ObjectId(conversation_id)})
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Get recent conversations"""
        return list(self.conversations.find().sort("created_at", -1).limit(limit))
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        total_conversations = self.conversations.count_documents({})
        
        # Calculate total messages across all conversations
        pipeline = [
            {"$group": {
                "_id": None,
                "total_messages": {"$sum": "$total_messages"}
            }}
        ]
        msg_result = list(self.conversations.aggregate(pipeline))
        total_messages = msg_result[0]["total_messages"] if msg_result else 0
        
        # Average sentiment from overall_sentiment.average_sentiment_score
        pipeline = [
            {"$group": {
                "_id": None,
                "avg_sentiment": {"$avg": "$overall_sentiment.average_sentiment_score"}
            }}
        ]
        avg_result = list(self.conversations.aggregate(pipeline))
        avg_sentiment = avg_result[0]["avg_sentiment"] if avg_result else 0
        
        return {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "average_sentiment": round(avg_sentiment, 3) if avg_sentiment else 0
        }
    
    def search_by_sentiment_direction(self, direction: str) -> List[Dict]:
        """
        Search conversations by overall emotional direction
        
        Args:
            direction: e.g., "evolved_positive", "predominantly_negative", etc.
        """
        return list(self.conversations.find({
            "overall_sentiment.overall_emotional_direction": direction
        }))
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✅ MongoDB connection closed")