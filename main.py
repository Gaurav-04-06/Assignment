from src.services import ChatService
from src.ui.display import ConsoleDisplay
from src.core.conversation import ConversationManager
from config import Config
from database import DatabaseManager

def display_welcome():
    """Show welcome message"""
    ConsoleDisplay.display_header("🎓 LIAPLUS ASSIGNMENT: MODULAR CHATBOT")
    print(f"✅ Using OpenAI {Config.OPENAI_MODEL}")
    print("\n💬 Type your messages below")
    print("🚪 Type 'quit' to exit without saving")
    print("👋 Type 'bye' or 'goodbye' to end and save conversation")
    print("📊 Type 'stats' to see database statistics\n")

def get_user_id() -> str:
    """Get user ID from input"""
    user_id = input("Enter your user ID (or press Enter for 'anonymous'): ").strip()
    return user_id if user_id else "anonymous"

def handle_stats():
    """Display database statistics"""
    try:
        db = DatabaseManager()
        stats = db.get_statistics()
        ConsoleDisplay.display_statistics(stats)
    except Exception as e:
        print(f"❌ Error retrieving statistics: {e}")

def main():
    """Run the CLI chatbot"""
    display_welcome()
    
    user_id = get_user_id()
    chat_service = ChatService(user_id=user_id)
    
    while chat_service.chatbot.chat_active:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Exiting...")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            print("\n👋 Exiting without saving conversation...")
            cost = chat_service.chatbot.get_cost_estimate()
            ConsoleDisplay.display_cost(cost)
            break
        
        if user_input.lower() == 'stats':
            handle_stats()
            continue
        
        # Send message
        print("\n⏳ Processing...")
        response_data = chat_service.send_message(user_input)
        
        # Display response
        ConsoleDisplay.display_response(response_data)
        
        # Check if chat ended
        if not chat_service.chatbot.chat_active:
            print("\n✅ Conversation completed!")
            conversation_id = chat_service.end_conversation()
            if conversation_id:
                print(f"💾 Conversation saved with ID: {conversation_id}")
            
            cost = chat_service.chatbot.get_cost_estimate()
            ConsoleDisplay.display_cost(cost)
            
            # Ask to continue
            if input("\n🔄 Start new conversation? (y/n): ").lower() == 'y':
                chat_service = ChatService(user_id=user_id)
            else:
                break

if __name__ == "__main__":
    try:
        Config.validate()
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        print("👋 Thank you for using LiaPlus AI!")
