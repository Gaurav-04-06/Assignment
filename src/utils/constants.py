"""Constants and configuration values"""

# Sentiment Score Thresholds
SENTIMENT_THRESHOLDS = {
    "strongly_positive": (0.8, 1.0),
    "positive": (0.3, 0.7),
    "neutral": (-0.2, 0.2),
    "negative": (-0.7, -0.3),
    "strongly_negative": (-1.0, -0.8)
}

# API Costs (per 1M tokens)
API_COSTS = {
    "input": 0.15,
    "output": 0.60
}

# Sentiment Classifications
SENTIMENT_TYPES = ["positive", "negative", "neutral"]
EMOTIONAL_DIRECTIONS = [
    "evolved_positive",
    "evolved_negative",
    "predominantly_positive",
    "predominantly_negative",
    "neutral",
    "mixed"
]

# Chat Configuration
DEFAULT_TEMPERATURE = 0.7
RESPONSE_FORMAT = {"type": "json_object"}
