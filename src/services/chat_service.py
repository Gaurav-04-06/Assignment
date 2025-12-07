"""Services layer for business logic orchestration"""

from typing import Dict, Optional
from datetime import datetime
from src.core.chatbot import SentimentChatbot
from src.core.conversation import ConversationManager
from database import DatabaseManager


class ChatService:
    """High-level chat service combining chatbot and persistence"""
    
    def __init__(self, user_id: str = "anonymous"):
        self.chatbot = SentimentChatbot(user_id=user_id)
        self.conversation_manager = ConversationManager(DatabaseManager())
        self.user_id = user_id
    
    def send_message(self, message: str) -> Dict:
        """Send message through chatbot"""
        return self.chatbot.send_message(message)
    
    def end_conversation(self) -> Optional[str]:
        """Save and end conversation"""
        if self.chatbot.conversation_summary:
            try:
                conversation_id = self.conversation_manager.save_conversation(
                    user_id=self.user_id,
                    messages=self.chatbot.conversation_history,
                    summary=self.chatbot.conversation_summary,
                    created_at=self.chatbot.conversation_start
                )
                return conversation_id
            except Exception as e:
                print(f"❌ Error saving conversation: {e}")
                return None
        return None
    
    def get_metrics(self) -> Dict:
        """Get current conversation metrics"""
        return {
            "message_count": self.chatbot.get_message_count(),
            "tokens": self.chatbot.total_input_tokens + self.chatbot.total_output_tokens,
            "cost": self.chatbot.get_cost_estimate()['total_cost'],
            "duration": (datetime.utcnow() - self.chatbot.conversation_start).total_seconds()
        }
