"""
Refactored app.py - Streamlit UI using modular architecture
"""

import streamlit as st
from datetime import datetime
from src.services import ChatService
from src.ui.components import UIStyles, ChartBuilder, MessageRenderer
from src.utils import SentimentUtils
from config import Config

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="LiaPlus AI • Enterprise Support",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# STYLING
# ============================================================================

st.markdown(UIStyles.get_dark_theme(), unsafe_allow_html=True)

# ============================================================================
# INITIALIZATION
# ============================================================================

try:
    Config.validate()
except Exception as e:
    st.error(f"⚠️ Configuration Error: {e}")
    st.stop()

@st.cache_resource
def get_chat_service():
    """Initialize chat service"""
    return ChatService()

# ============================================================================
# SESSION STATE
# ============================================================================

if "chat_service" not in st.session_state:
    st.session_state.chat_service = get_chat_service()
    st.session_state.conversation_ended = False

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown('<div style="text-align: center; font-size: 1.5rem; font-weight: bold;">✨ LiaPlus AI</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 👤 User Identity")
    user_id = st.text_input("User ID", value="anonymous", label_visibility="collapsed")
    
    st.markdown("### 📊 Current Session")
    metrics = st.session_state.chat_service.get_metrics()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", metrics['message_count'])
    with col2:
        st.metric("Tokens", int(metrics['tokens']))
    st.metric("Est. Cost", f"${metrics['cost']:.6f}")
    
    st.markdown("---")
    
    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.chat_service = ChatService()
        st.session_state.conversation_ended = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: rgba(255,255,255,0.5); font-size: 0.9rem;'><strong>LiaPlus AI Assignment</strong><br>Powered by GPT-4o-mini</div>", unsafe_allow_html=True)

# ============================================================================
# MAIN INTERFACE
# ============================================================================

st.markdown(MessageRenderer.render_header(
    "✨ LiaPlus AI Enterprise Support",
    "Your intelligent assistant with real-time sentiment analysis"
), unsafe_allow_html=True)

# Display conversation ended message
if st.session_state.conversation_ended:
    st.success("✅ **Conversation Successfully Completed!** Your chat has been saved.")
    
    summary = st.session_state.chat_service.chatbot.conversation_summary
    if summary:
        st.subheader("📋 Conversation Summary")
        
        full_sentiment = summary.get('full_conversation_sentiment', {})
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Direction", full_sentiment.get('overall_emotional_direction', 'N/A'))
        with col2:
            st.metric("Avg Sentiment Score", f"{full_sentiment.get('average_sentiment_score', 0):.2f}")
        with col3:
            st.metric("Total Messages", summary.get('total_user_messages', 0))
        
        st.info(full_sentiment.get('narrative_description', ''))
        
        # Sentiment journey
        st.subheader("🛣️ Sentiment Journey")
        journey = summary.get('sentiment_journey', {})
        
        col1, col2, col3 = st.columns(3)
        for idx, (phase, col) in enumerate(zip(['opening_phase', 'middle_phase', 'closing_phase'], [col1, col2, col3])):
            phase_data = journey.get(phase, {})
            with col:
                st.metric(
                    phase.replace('_', ' ').title(),
                    phase_data.get('sentiment', 'N/A'),
                    delta=f"{phase_data.get('score', 0):.2f}"
                )
        
        # Key moments
        st.subheader("⭐ Key Emotional Moments")
        for moment in summary.get('key_emotional_moments', []):
            st.write(f"**Message #{moment['message_number']}** - {moment['sentiment_classification']} "
                    f"(score: {moment['sentiment_score']:.2f})")
            st.caption(moment['significance'])
        
        # Insights
        st.subheader("💡 Insights")
        for insight in summary.get('insights', []):
            st.write(f"• {insight}")
    
    st.info("💬 **Ready for your next conversation?** Click 'New Conversation' in the sidebar to start fresh!")

# Display chat messages
for message in st.session_state.chat_service.chatbot.conversation_history:
    with st.chat_message("user", avatar="👤"):
        st.write(message['user_message'])
    
    with st.chat_message("assistant", avatar="🤖"):
        st.write(message['bot_response'])

# Chat input
if not st.session_state.conversation_ended:
    if prompt := st.chat_input("💬 Type your message here..."):
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.write(prompt)
        
        # Get bot response
        with st.spinner("🤖 Thinking..."):
            response = st.session_state.chat_service.send_message(prompt)
        
        # Display bot response
        with st.chat_message("assistant", avatar="🤖"):
            st.write(response['response'])
        
        # Check if conversation ended
        if not st.session_state.chat_service.chatbot.chat_active:
            st.session_state.conversation_ended = True
            st.rerun()
        else:
            st.rerun()
else:
    if st.button("🔄 Start New Chat", type="primary", use_container_width=True):
        st.session_state.chat_service = ChatService()
        st.session_state.conversation_ended = False
        st.rerun()

# Welcome screen
if not st.session_state.conversation_ended and len(st.session_state.chat_service.chatbot.conversation_history) == 0:
    st.markdown("---")
    st.markdown(MessageRenderer.render_welcome_card(), unsafe_allow_html=True)
