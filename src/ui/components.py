"""UI components and rendering utilities"""

import plotly.graph_objects as go
from typing import List, Dict


class UIStyles:
    """Centralized UI styling"""
    
    DARK_THEME_CSS = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

        /* Bluish gradient background */
        .stApp {
            background: linear-gradient(135deg, #0a2540 0%, #0d3b66 50%, #0f4c75 100%);
            background-attachment: fixed;
        }

        /* Main container padding */
        .main .block-container {
            padding: 2rem 3rem;
            max-width: 1400px;
        }

        /* NAVBAR */
        .navbar {
            width: 100%;
            background: rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            backdrop-filter: blur(20px);
            z-index: 9999;
        }

        .navbar-title {
            font-size: 1.6rem;
            font-weight: 800;
            background: linear-gradient(135deg, #4dabf7 0%, #1c7ed6 50%, #74c0fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }

        /* HIDE SIDEBAR COMPLETELY */
        [data-testid="stSidebar"] {
            display: none !important;
        }

        /* Chat and components theme adjustments */
        .header-container {
            background: rgba(255, 255, 255, 0.04);
            border-radius: 24px;
            padding: 2rem 2.5rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.06);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }

        .main-title {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #4dabf7 0%, #1c7ed6 50%, #74c0fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }

        .subtitle {
            color: rgba(255, 255, 255, 0.7);
            font-size: 1.1rem;
        }

        .stChatMessage {
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 20px !important;
            padding: 1.5rem !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        footer { visibility: hidden; }
    </style>
    """
    
    @classmethod
    def get_dark_theme(cls) -> str:
        """Get dark theme CSS"""
        return cls.DARK_THEME_CSS


class ChartBuilder:
    """Build interactive charts for sentiment visualization"""
    
    @staticmethod
    def create_sentiment_chart(sentiment_history: List[Dict]) -> go.Figure:
        """
        Create sentiment trend chart
        
        Args:
            sentiment_history: List of sentiment data points
            
        Returns:
            Plotly figure object
        """
        if not sentiment_history:
            return None
        
        scores = [s['score'] for s in sentiment_history]
        messages = list(range(1, len(scores) + 1))
        sentiments = [s['sentiment'] for s in sentiment_history]
        colors = [
            '#10b981' if s == 'positive' else '#ef4444' if s == 'negative' else '#9ca3af'
            for s in sentiments
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=messages,
            y=scores,
            mode='lines+markers',
            name='Sentiment Score',
            line=dict(color='rgba(102, 126, 234, 0.8)', width=3),
            marker=dict(size=10, color=colors, line=dict(color='white', width=2)),
            hovertemplate='<b>Message %{x}</b><br>Score: %{y:.2f}<extra></extra>'
        ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="rgba(255, 255, 255, 0.3)")
        fig.add_hline(y=0.3, line_dash="dot", line_color="rgba(16, 185, 129, 0.3)")
        fig.add_hline(y=-0.3, line_dash="dot", line_color="rgba(239, 68, 68, 0.3)")
        
        fig.update_layout(
            title="Sentiment Trend Across Conversation",
            xaxis_title="Message Number",
            yaxis_title="Sentiment Score",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            hovermode='x unified',
            yaxis=dict(range=[-1.1, 1.1], gridcolor='rgba(255, 255, 255, 0.1)'),
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
            height=350
        )
        
        return fig


class MessageRenderer:
    """Render messages in UI format"""
    
    @staticmethod
    def render_header(title: str, subtitle: str) -> str:
        """Render header section"""
        return f"""
        <div class="header-container">
            <div class="main-title">{title}</div>
            <div class="subtitle">{subtitle}</div>
        </div>
        """
    
    @staticmethod
    def render_welcome_card() -> str:
        """Render welcome card"""
        return """
        <div class="welcome-card">
            <h3>👋 Welcome to LiaPlus AI Enterprise Support!</h3>
            <p>I'm your intelligent AI assistant with <strong>real-time sentiment analysis</strong>.</p>
            <p><strong>Start typing below to begin our conversation.</strong></p>
            <div style="margin-top: 2rem; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
                <div style="text-align: center;"><div style="font-size: 2rem;">🎯</div><div style="color: rgba(255,255,255,0.7); margin-top: 0.5rem;">Intelligent Support</div></div>
                <div style="text-align: center;"><div style="font-size: 2rem;">⚡</div><div style="color: rgba(255,255,255,0.7); margin-top: 0.5rem;">Instant Responses</div></div>
                <div style="text-align: center;"><div style="font-size: 2rem;">📊</div><div style="color: rgba(255,255,255,0.7); margin-top: 0.5rem;">Per-Message Sentiment</div></div>
                <div style="text-align: center;"><div style="font-size: 2rem;">🔒</div><div style="color: rgba(255,255,255,0.7); margin-top: 0.5rem;">Secure & Private</div></div>
            </div>
        </div>
        """
