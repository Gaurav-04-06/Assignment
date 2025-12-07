"""Conversation management and tracking"""

from typing import List, Dict, Optional
from datetime import datetime
from database import DatabaseManager


class ConversationManager:
    """Manages conversation persistence and retrieval"""
    
    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()
    
    def save_conversation(self, user_id: str, messages: List[Dict], 
                         summary: Dict, created_at: datetime) -> str:
        """
        Save complete conversation to database
        
        Args:
            user_id: User identifier
            messages: List of message exchanges
            summary: Conversation summary with sentiment
            created_at: When conversation started
            
        Returns:
            conversation_id: ID of saved conversation
        """
        if self.db.conversations is None:
            raise ConnectionError("Database not connected")
        
        return self.db.save_complete_conversation(
            user_id=user_id,
            messages=messages,
            conversation_summary=summary,
            created_at=created_at
        )
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Retrieve a conversation by ID"""
        return self.db.get_conversation(conversation_id)
    
    def get_user_conversations(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get recent conversations for a user"""
        if self.db.conversations is None:
            return []
        
        return list(self.db.conversations.find(
            {"user_id": user_id}
        ).sort("created_at", -1).limit(limit))
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        return self.db.get_statistics()
    
    def search_by_sentiment(self, direction: str) -> List[Dict]:
        """Search conversations by emotional direction"""
        return self.db.search_by_sentiment_direction(direction)
