"""
Streamlit analytics dashboard for AI Digital Call Center.
"""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"


def fetch_analytics() -> dict:
    """
    Fetch analytics data from API.
    
    Returns:
        Analytics data dictionary
    """
    try:
        response = requests.get(f"{API_BASE_URL}/analytics", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def main():
    """Main dashboard application."""
    st.set_page_config(
        page_title="Analytics Dashboard - AI Call Center",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 AI Digital Call Center - Analytics Dashboard")
    st.markdown("**Real-time metrics and performance analytics**")
    
    # Fetch analytics
    analytics_data = fetch_analytics()
    
    if not analytics_data:
        st.error("Unable to fetch analytics data. Please ensure the backend API is running.")
        st.info("Start the backend server with: `python backend/main.py` or `uvicorn backend.main:app`")
        return
    
    # Key Metrics Row
    st.subheader("📈 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Conversations",
            analytics_data.get("total_conversations", 0),
            help="Total number of conversations handled"
        )
    
    with col2:
        resolved = analytics_data.get("total_resolved", 0)
        total = analytics_data.get("total_conversations", 1)
        resolution_rate = (resolved / total * 100) if total > 0 else 0
        st.metric(
            "Resolved",
            resolved,
            delta=f"{resolution_rate:.1f}%",
            help="Conversations successfully resolved"
        )
    
    with col3:
        escalated = analytics_data.get("total_escalated", 0)
        escalation_rate = analytics_data.get("escalation_rate", 0)
        st.metric(
            "Escalated",
            escalated,
            delta=f"{escalation_rate:.1f}%",
            delta_color="inverse",
            help="Conversations escalated to human agents"
        )
    
    with col4:
        avg_csat = analytics_data.get("average_csat")
        if avg_csat:
            st.metric(
                "Avg CSAT",
                f"{avg_csat:.2f}/5.0",
                help="Average Customer Satisfaction Score"
            )
        else:
            st.metric("Avg CSAT", "N/A", help="No feedback data available")
    
    with col5:
        avg_confidence = analytics_data.get("average_confidence")
        if avg_confidence:
            st.metric(
                "Avg Confidence",
                f"{avg_confidence * 100:.1f}%",
                help="Average agent confidence score"
            )
        else:
            st.metric("Avg Confidence", "N/A")
    
    st.divider()
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 Conversations by Agent Type")
        agent_data = analytics_data.get("conversations_by_agent", {})
        
        if agent_data:
            agent_df = pd.DataFrame([
                {"Agent Type": "Primary", "Count": agent_data.get("primary", 0)},
                {"Agent Type": "Supervisor", "Count": agent_data.get("supervisor", 0)},
                {"Agent Type": "Human", "Count": agent_data.get("human", 0)}
            ])
            
            fig = px.bar(
                agent_df,
                x="Agent Type",
                y="Count",
                color="Agent Type",
                color_discrete_map={
                    "Primary": "#1f77b4",
                    "Supervisor": "#ff7f0e",
                    "Human": "#2ca02c"
                },
                title="Conversation Distribution by Agent"
            )
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No agent data available")
    
    with col2:
        st.subheader("💬 Conversations by Intent")
        intent_data = analytics_data.get("conversations_by_intent", {})
        
        if intent_data:
            intent_df = pd.DataFrame([
                {"Intent": k.replace("_", " ").title(), "Count": v}
                for k, v in intent_data.items()
            ])
            
            # Sort by count
            intent_df = intent_df.sort_values("Count", ascending=False).head(10)
            
            fig = px.pie(
                intent_df,
                values="Count",
                names="Intent",
                title="Intent Distribution"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No intent data available")
    
    st.divider()
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("😊 Conversations by Sentiment")
        sentiment_data = analytics_data.get("conversations_by_sentiment", {})
        
        if sentiment_data:
            sentiment_df = pd.DataFrame([
                {"Sentiment": k.title(), "Count": v}
                for k, v in sentiment_data.items()
            ])
            
            color_map = {
                "Positive": "#2ca02c",
                "Negative": "#d62728",
                "Neutral": "#7f7f7f"
            }
            
            fig = px.bar(
                sentiment_df,
                x="Sentiment",
                y="Count",
                color="Sentiment",
                color_discrete_map=color_map,
                title="Sentiment Distribution"
            )
            fig.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sentiment data available")
    
    with col2:
        st.subheader("⏱️ Performance Metrics")
        
        metrics_data = []
        
        avg_resolution_time = analytics_data.get("average_resolution_time_seconds")
        if avg_resolution_time:
            minutes = avg_resolution_time / 60
            metrics_data.append({
                "Metric": "Avg Resolution Time",
                "Value": f"{minutes:.1f} min"
            })
        else:
            metrics_data.append({
                "Metric": "Avg Resolution Time",
                "Value": "N/A"
            })
        
        escalation_rate = analytics_data.get("escalation_rate", 0)
        metrics_data.append({
            "Metric": "Escalation Rate",
            "Value": f"{escalation_rate:.1f}%"
        })
        
        resolution_rate = (
            (analytics_data.get("total_resolved", 0) / 
             analytics_data.get("total_conversations", 1)) * 100
            if analytics_data.get("total_conversations", 0) > 0 else 0
        )
        metrics_data.append({
            "Metric": "Resolution Rate",
            "Value": f"{resolution_rate:.1f}%"
        })
        
        metrics_df = pd.DataFrame(metrics_data)
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Raw Data Section
    with st.expander("📋 Raw Analytics Data"):
        st.json(analytics_data)
    
    # Refresh button
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "AI Digital Call Center Analytics Dashboard | "
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

