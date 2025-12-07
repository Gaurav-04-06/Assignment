from typing import List, Optional, Dict
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class SentimentData:
    """Data class for sentiment information"""
    classification: str
    score: float
    confidence: str
    key_indicators: List[str]
    brief_reasoning: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)

@dataclass
class Message:
    """Data class for a message exchange"""
    conversation_id: str
    user_message: str
    bot_response: str
    sentiment: SentimentData
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for MongoDB"""
        return {
            "conversation_id": self.conversation_id,
            "user_message": self.user_message,
            "bot_response": self.bot_response,
            "sentiment": self.sentiment.to_dict(),
            "timestamp": self.timestamp
        }

@dataclass
class Conversation:
    """Data class for a conversation"""
    user_id: str
    created_at: datetime = None
    updated_at: datetime = None
    status: str = "active"
    total_messages: int = 0
    sentiment_scores: List[float] = None
    summary: Optional[Dict] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
        if self.sentiment_scores is None:
            self.sentiment_scores = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for MongoDB"""
        return asdict(self)