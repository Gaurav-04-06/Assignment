"""Chatbot core logic - handles OpenAI API calls"""

import json
from typing import List, Dict, Optional
from datetime import datetime
from openai import OpenAI
from config import Config
from .prompts import Prompts


class SentimentChatbot:
    """Main chatbot class for handling conversations"""
    
    def __init__(self, user_id: str = "anonymous"):
        self.user_id = user_id
        self.conversation_history: List[Dict] = []
        self.chat_active = True
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.conversation_start = datetime.utcnow()
        self.conversation_summary: Optional[Dict] = None
        
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
        
        print(f"💬 Starting new conversation for user: {user_id}")
    
    def _clean_json_response(self, response_text: str) -> str:
        """Remove markdown code blocks and clean JSON response"""
        response_text = response_text.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]
        
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        return response_text.strip()
    
    def _build_messages(self) -> List[Dict]:
        """Build OpenAI messages format from conversation history"""
        messages = [{"role": "system", "content": Prompts.get_system_prompt()}]
        
        for msg in self.conversation_history:
            messages.append({"role": "user", "content": msg['user_message']})
            messages.append({"role": "assistant", "content": json.dumps({
                "response": msg['bot_response']
            })})
        
        return messages
    
    def send_message(self, user_message: str) -> Dict:
        """
        Send a message and get response from OpenAI
        
        Args:
            user_message: User's input message
            
        Returns:
            Response dictionary with bot response and metadata
        """
        try:
            messages = self._build_messages()
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            # Track token usage
            self.total_input_tokens += response.usage.prompt_tokens
            self.total_output_tokens += response.usage.completion_tokens
            
            response_text = response.choices[0].message.content
            cleaned_response = self._clean_json_response(response_text)
            parsed_response = json.loads(cleaned_response)
            
            # Store in conversation history
            self.conversation_history.append({
                'user_message': user_message,
                'bot_response': parsed_response['response'],
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Check if conversation is ending
            if 'conversation_summary' in parsed_response:
                self.chat_active = False
                self.conversation_summary = parsed_response['conversation_summary']
            
            return parsed_response
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parse Error: {e}")
            return {
                "response": "I apologize, but I encountered an error. Could you please rephrase?",
                "error": str(e)
            }
        except Exception as e:
            print(f"❌ Error: {e}")
            return {
                "response": "I apologize, but I encountered an unexpected error.",
                "error": str(e)
            }
    
    def get_cost_estimate(self) -> Dict:
        """Calculate token costs"""
        input_cost = (self.total_input_tokens / 1_000_000) * 0.15
        output_cost = (self.total_output_tokens / 1_000_000) * 0.60
        total_cost = input_cost + output_cost
        
        return {
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost
        }
    
    def get_message_count(self) -> int:
        """Get total number of messages in conversation"""
        return len(self.conversation_history)
    
    def get_last_message(self) -> Optional[Dict]:
        """Get the last message in conversation"""
        return self.conversation_history[-1] if self.conversation_history else None
