"""
Pydantic schemas for API request/response validation.
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    """Schema for incoming message request."""
    message: str = Field(..., description="Customer message content")
    session_id: Optional[str] = Field(None, description="Conversation session ID")
    customer_id: Optional[str] = Field(None, description="Customer identifier")


class MessageResponse(BaseModel):
    """Schema for message response."""
    session_id: str
    response: str
    agent_type: str
    agent_name: str
    confidence: float
    intent: str
    intent_label: str
    sentiment_score: float
    sentiment_label: str
    needs_escalation: bool
    escalation_reason: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class ConversationResponse(BaseModel):
    """Schema for conversation response."""
    session_id: str
    messages: List[dict]
    status: str
    started_at: datetime
    primary_agent_handled: bool
    supervisor_agent_handled: bool
    human_agent_handled: bool


class FeedbackRequest(BaseModel):
    """Schema for feedback submission."""
    session_id: str
    csat_score: int = Field(..., ge=1, le=5, description="CSAT score from 1 to 5")
    feedback_text: Optional[str] = None


class FeedbackResponse(BaseModel):
    """Schema for feedback response."""
    session_id: str
    csat_score: int
    feedback_text: Optional[str]
    submitted_at: datetime


class AnalyticsResponse(BaseModel):
    """Schema for analytics data."""
    total_conversations: int
    total_resolved: int
    total_escalated: int
    average_csat: Optional[float]
    average_resolution_time_seconds: Optional[float]
    average_confidence: Optional[float]
    escalation_rate: float
    conversations_by_agent: dict
    conversations_by_intent: dict
    conversations_by_sentiment: dict


