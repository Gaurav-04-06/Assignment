"""Utility functions for JSON, text formatting, etc."""

import json
from typing import Dict, Any


class JSONUtils:
    """JSON processing utilities"""
    
    @staticmethod
    def clean_json_response(response_text: str) -> str:
        """Remove markdown code blocks from JSON response"""
        response_text = response_text.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]
        
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        return response_text.strip()
    
    @staticmethod
    def safe_parse_json(json_str: str) -> Dict[str, Any]:
        """Safely parse JSON with error handling"""
        try:
            cleaned = JSONUtils.clean_json_response(json_str)
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            return {"error": f"JSON Parse Error: {e}"}


class SentimentUtils:
    """Sentiment analysis utilities"""
    
    SENTIMENT_EMOJIS = {
        "positive": "😊",
        "negative": "😔",
        "neutral": "😐"
    }
    
    SENTIMENT_COLORS = {
        "positive": "#10b981",
        "negative": "#ef4444",
        "neutral": "#9ca3af"
    }
    
    @staticmethod
    def get_emoji(score: float) -> str:
        """Get emoji based on sentiment score"""
        if score > 0.5:
            return "😊"
        elif score > 0.2:
            return "🙂"
        elif score > -0.2:
            return "😐"
        elif score > -0.5:
            return "😕"
        else:
            return "😔"
    
    @staticmethod
    def get_color(sentiment: str) -> str:
        """Get color based on sentiment type"""
        return SentimentUtils.SENTIMENT_COLORS.get(sentiment, "#9ca3af")
    
    @staticmethod
    def classify_direction(score: float) -> str:
        """Classify sentiment direction"""
        if score > 0.3:
            return "positive"
        elif score < -0.3:
            return "negative"
        else:
            return "neutral"


class FormatUtils:
    """Text formatting utilities"""
    
    @staticmethod
    def format_token_count(count: int) -> str:
        """Format token count as human readable"""
        if count >= 1_000_000:
            return f"{count / 1_000_000:.2f}M"
        elif count >= 1_000:
            return f"{count / 1_000:.2f}K"
        return str(count)
    
    @staticmethod
    def format_cost(cost: float) -> str:
        """Format cost as currency"""
        return f"${cost:.6f}"
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format duration as human readable"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"
