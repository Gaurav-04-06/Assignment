import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the chatbot"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "liaplus_chatbot")
    
    # Collections
    CONVERSATIONS_COLLECTION = "conversations"
    MESSAGES_COLLECTION = "messages"
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        errors = []
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY not found in .env file")
        if not cls.MONGODB_URI:
            errors.append("MONGODB_URI not found in .env file")
        if not cls.MONGODB_DATABASE:
            errors.append("MONGODB_DATABASE not found in .env file")
        
        if errors:
            print("\n❌ Configuration Errors:")
            for error in errors:
                print(f"   • {error}")
            print("\n💡 Please check your .env file has these variables:")
            print("   OPENAI_API_KEY=your_key_here")
            print("   MONGODB_URI=your_mongodb_connection_string")
            print("   MONGODB_DATABASE=your_database_name")
            print()
            raise ValueError("Missing required configuration")
        
        print("✅ Configuration validated successfully")
        return True