"""Display and formatting for console and terminal output"""

from typing import Dict, List, Optional


class ConsoleDisplay:
    """Terminal/console output formatting"""
    
    @staticmethod
    def display_header(title: str, width: int = 70):
        """Display formatted header"""
        print("=" * width)
        print(title.center(width))
        print("=" * width)
    
    @staticmethod
    def display_response(response_data: Dict):
        """Display bot response with formatting"""
        ConsoleDisplay.display_header("🤖 BOT RESPONSE")
        print(response_data.get('response', 'No response'))
        
        if 'conversation_summary' in response_data:
            ConsoleDisplay._display_summary(response_data['conversation_summary'])
        
        print("=" * 70 + "\n")
    
    @staticmethod
    def _display_summary(summary: Dict):
        """Display conversation summary"""
        print("\n" + "=" * 70)
        print("📋 OVERALL CONVERSATION SUMMARY:".center(70))
        print("=" * 70)
        
        print(f"\n📈 Total User Messages: {summary.get('total_user_messages', 'N/A')}")
        
        full_sentiment = summary.get('full_conversation_sentiment', {})
        print(f"\n🎯 Overall Emotional Direction: {full_sentiment.get('overall_emotional_direction', 'N/A')}")
        print(f"📊 Average Sentiment Score: {full_sentiment.get('average_sentiment_score', 'N/A')}")
        print(f"📝 Description: {full_sentiment.get('narrative_description', 'N/A')}")
        
        journey = summary.get('sentiment_journey', {})
        print(f"\n🛣️ Sentiment Journey:")
        
        for phase in ['opening_phase', 'middle_phase', 'closing_phase']:
            phase_data = journey.get(phase, {})
            phase_name = phase.replace('_phase', '').replace('_', ' ').title()
            print(f"  • {phase_name}: {phase_data.get('sentiment', 'N/A')} (score: {phase_data.get('score', 'N/A')})")
            print(f"    {phase_data.get('description', 'N/A')}")
        
        print(f"\n🔄 Mood Shift Analysis:")
        print(f"  {journey.get('mood_shift_analysis', 'N/A')}")
        
        print(f"\n⭐ Key Emotional Moments:")
        for moment in summary.get('key_emotional_moments', []):
            print(f"  Message #{moment['message_number']}: {moment['sentiment_classification']} "
                  f"(score: {moment['sentiment_score']})")
            print(f"    → {moment['significance']}")
        
        print(f"\n💡 Insights:")
        for insight in summary.get('insights', []):
            print(f"  • {insight}")
    
    @staticmethod
    def display_statistics(stats: Dict):
        """Display database statistics"""
        ConsoleDisplay.display_header("📊 DATABASE STATISTICS")
        print(f"Total Conversations: {stats.get('total_conversations', 0)}")
        print(f"Total Messages: {stats.get('total_messages', 0)}")
        print(f"Average Sentiment: {stats.get('average_sentiment', 0):.3f}")
        print("=" * 70 + "\n")
    
    @staticmethod
    def display_cost(cost_data: Dict):
        """Display cost breakdown"""
        print("\n" + "=" * 70)
        print("💰 COST BREAKDOWN".center(70))
        print("=" * 70)
        print(f"Input Tokens:   {cost_data['input_tokens']:>10,}")
        print(f"Output Tokens:  {cost_data['output_tokens']:>10,}")
        print(f"Total Tokens:   {cost_data['total_tokens']:>10,}")
        print(f"\nInput Cost:     ${cost_data['input_cost']:>9.6f}")
        print(f"Output Cost:    ${cost_data['output_cost']:>9.6f}")
        print(f"Total Cost:     ${cost_data['total_cost']:>9.6f}")
        print("=" * 70 + "\n")
