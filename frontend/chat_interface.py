"""
Streamlit chat interface for AI Digital Call Center.
"""
import streamlit as st
import requests
import json
from datetime import datetime
from typing import Optional

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"


def init_session_state():
    """Initialize session state variables."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False


def send_message(message: str, session_id: Optional[str] = None) -> dict:
    """
    Send message to API and get response.
    
    Args:
        message: User's message
        session_id: Session ID if continuing conversation
        
    Returns:
        API response dictionary
    """
    try:
        payload = {
            "message": message,
            "session_id": session_id
        }
        
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": f"API Error: {response.status_code}",
                "response": "I apologize, but I'm experiencing technical difficulties. Please try again."
            }
    
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "response": "I apologize, but I'm unable to connect to the server. Please check your connection."
        }


def display_message(role: str, content: str, metadata: Optional[dict] = None):
    """
    Display a message in the chat interface.
    
    Args:
        role: Message role (customer, agent, etc.)
        content: Message content
        metadata: Optional metadata (confidence, intent, etc.)
    """
    if role == "customer":
        with st.chat_message("user"):
            st.write(content)
    else:
        agent_name = metadata.get("agent_name", "AI Agent") if metadata else "AI Agent"
        with st.chat_message("assistant"):
            st.write(content)
            
            # Display metadata if available
            if metadata:
                with st.expander("Agent Details"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Confidence", f"{metadata.get('confidence', 0) * 100:.1f}%")
                        st.metric("Intent", metadata.get("intent_label", "N/A"))
                    with col2:
                        st.metric("Sentiment", metadata.get("sentiment_label", "N/A"))
                        if metadata.get("needs_escalation"):
                            st.warning("⚠️ Escalation Required")


def main():
    """Main chat interface application."""
    st.set_page_config(
        page_title="AI Digital Call Center",
        page_icon="💬",
        layout="wide"
    )
    
    # Initialize session state
    init_session_state()
    
    # Title and description
    st.title("🤖 AI Digital Call Center")
    st.markdown("**Enterprise-grade multi-agent AI customer support system**")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Controls")
        
        if st.button("🔄 New Conversation", use_container_width=True):
            st.session_state.session_id = None
            st.session_state.messages = []
            st.session_state.conversation_started = False
            st.rerun()
        
        st.divider()
        
        if st.session_state.session_id:
            st.success(f"**Session ID:**\n`{st.session_state.session_id[:20]}...`")
        else:
            st.info("No active session")
        
        st.divider()
        
        st.markdown("### About")
        st.markdown("""
        This system uses a multi-agent AI architecture:
        - **Primary Agent**: First-line support
        - **Supervisor Agent**: Complex queries
        - **Escalation Agent**: Human handoff
        """)
        
        st.markdown("### Features")
        st.markdown("""
        - ✅ Intent detection
        - ✅ Sentiment analysis
        - ✅ Confidence scoring
        - ✅ Intelligent escalation
        - ✅ Context memory
        """)
    
    # Chat interface
    if not st.session_state.conversation_started:
        st.info("👋 Welcome! Start a conversation by typing a message below.")
    
    # Display chat history
    for msg in st.session_state.messages:
        display_message(
            role=msg["role"],
            content=msg["content"],
            metadata=msg.get("metadata")
        )
    
    # Chat input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({
            "role": "customer",
            "content": user_input
        })
        st.session_state.conversation_started = True
        
        # Display user message
        display_message("customer", user_input)
        
        # Send to API and get response
        with st.spinner("🤔 Thinking..."):
            response = send_message(
                message=user_input,
                session_id=st.session_state.session_id
            )
        
        # Update session ID if provided
        if "session_id" in response:
            st.session_state.session_id = response["session_id"]
        
        # Extract response content
        if "error" in response:
            agent_response = response["response"]
            metadata = None
        else:
            agent_response = response["response"]
            metadata = {
                "agent_name": response.get("agent_name", "AI Agent"),
                "agent_type": response.get("agent_type", "primary"),
                "confidence": response.get("confidence", 0.0),
                "intent": response.get("intent", ""),
                "intent_label": response.get("intent_label", ""),
                "sentiment_label": response.get("sentiment_label", ""),
                "needs_escalation": response.get("needs_escalation", False),
                "escalation_reason": response.get("escalation_reason")
            }
        
        # Add agent response to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": agent_response,
            "metadata": metadata
        })
        
        # Display agent response
        display_message("assistant", agent_response, metadata)
        
        # Show escalation notice if needed
        if metadata and metadata.get("needs_escalation"):
            st.warning(f"⚠️ **Escalation:** {metadata.get('escalation_reason', 'Query escalated to supervisor')}")
        
        st.rerun()


if __name__ == "__main__":
    main()


