"""
FastAPI routes for the AI Digital Call Center API.
"""
from typing import List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from fastapi import APIRouter, Depends, HTTPException

from app.core.database import get_db
from app.models.database_models import Conversation, Message, Feedback, AgentMetric
from app.api.schemas import (
    MessageRequest, MessageResponse, ConversationResponse,
    FeedbackRequest, FeedbackResponse, AnalyticsResponse
)
from app.services.conversation_service import conversation_service


router = APIRouter()


@router.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest, db: Session = Depends(get_db)):
    """
    Process customer message and return AI agent response.
    """
    try:
        # Process message through conversation service
        result = await conversation_service.process_message(
            message=request.message,
            session_id=request.session_id,
            customer_id=request.customer_id,
            db=db
        )
        
        return MessageResponse(
            session_id=result["session_id"],
            response=result["response"],
            agent_type=result["agent_type"],
            agent_name=result["agent_name"],
            confidence=result["confidence"],
            intent=result["intent"],
            intent_label=result["intent_label"],
            sentiment_score=result["sentiment_score"],
            sentiment_label=result["sentiment_label"],
            needs_escalation=result.get("needs_escalation", False),
            escalation_reason=result.get("escalation_reason"),
            timestamp=result.get("timestamp", datetime.now())
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@router.get("/conversation/{session_id}", response_model=ConversationResponse)
async def get_conversation(session_id: str, db: Session = Depends(get_db)):
    """
    Get conversation history by session ID.
    """
    conversation = db.query(Conversation).filter(
        Conversation.session_id == session_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at).all()
    
    messages_data = [
        {
            "role": msg.role,
            "content": msg.content,
            "intent": msg.intent,
            "sentiment_label": msg.sentiment_label,
            "confidence_score": msg.confidence_score,
            "created_at": msg.created_at.isoformat()
        }
        for msg in messages
    ]
    
    return ConversationResponse(
        session_id=conversation.session_id,
        messages=messages_data,
        status=conversation.status,
        started_at=conversation.started_at,
        primary_agent_handled=conversation.primary_agent_handled,
        supervisor_agent_handled=conversation.supervisor_agent_handled,
        human_agent_handled=conversation.human_agent_handled
    )


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    """
    Submit customer satisfaction feedback (CSAT).
    """
    conversation = db.query(Conversation).filter(
        Conversation.session_id == request.session_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Check if feedback already exists
    existing_feedback = db.query(Feedback).filter(
        Feedback.conversation_id == conversation.id
    ).first()
    
    if existing_feedback:
        # Update existing feedback
        existing_feedback.csat_score = request.csat_score
        existing_feedback.feedback_text = request.feedback_text
        existing_feedback.submitted_at = datetime.now()
        db.commit()
        db.refresh(existing_feedback)
        
        return FeedbackResponse(
            session_id=request.session_id,
            csat_score=existing_feedback.csat_score,
            feedback_text=existing_feedback.feedback_text,
            submitted_at=existing_feedback.submitted_at
        )
    
    # Create new feedback
    feedback = Feedback(
        conversation_id=conversation.id,
        csat_score=request.csat_score,
        feedback_text=request.feedback_text
    )
    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return FeedbackResponse(
        session_id=request.session_id,
        csat_score=feedback.csat_score,
        feedback_text=feedback.feedback_text,
        submitted_at=feedback.submitted_at
    )


@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(db: Session = Depends(get_db)):
    """
    Get analytics and metrics for the dashboard.
    """
    # Total conversations
    total_conversations = db.query(Conversation).count()
    
    # Resolved conversations
    total_resolved = db.query(Conversation).filter(
        Conversation.status == "resolved"
    ).count()
    
    # Escalated conversations
    total_escalated = db.query(Conversation).filter(
        Conversation.human_agent_handled == True
    ).count()
    
    # Average CSAT
    avg_csat = db.query(func.avg(Feedback.csat_score)).scalar()
    
    # Average resolution time
    avg_resolution_time = db.query(
        func.avg(Conversation.resolution_time_seconds)
    ).filter(
        Conversation.resolution_time_seconds.isnot(None)
    ).scalar()
    
    # Average confidence
    avg_confidence = db.query(func.avg(Message.confidence_score)).filter(
        Message.confidence_score.isnot(None)
    ).scalar()
    
    # Escalation rate
    escalation_rate = (total_escalated / total_conversations * 100) if total_conversations > 0 else 0.0
    
    # Conversations by agent type
    conversations_by_agent = {
        "primary": db.query(Conversation).filter(
            Conversation.primary_agent_handled == True
        ).count(),
        "supervisor": db.query(Conversation).filter(
            Conversation.supervisor_agent_handled == True
        ).count(),
        "human": db.query(Conversation).filter(
            Conversation.human_agent_handled == True
        ).count()
    }
    
    # Conversations by intent
    intent_counts = db.query(
        Message.intent,
        func.count(Message.id).label("count")
    ).filter(
        Message.intent.isnot(None)
    ).group_by(Message.intent).all()
    
    conversations_by_intent = {intent: count for intent, count in intent_counts}
    
    # Conversations by sentiment
    sentiment_counts = db.query(
        Message.sentiment_label,
        func.count(Message.id).label("count")
    ).filter(
        Message.sentiment_label.isnot(None)
    ).group_by(Message.sentiment_label).all()
    
    conversations_by_sentiment = {sentiment: count for sentiment, count in sentiment_counts}
    
    return AnalyticsResponse(
        total_conversations=total_conversations,
        total_resolved=total_resolved,
        total_escalated=total_escalated,
        average_csat=float(avg_csat) if avg_csat else None,
        average_resolution_time_seconds=float(avg_resolution_time) if avg_resolution_time else None,
        average_confidence=float(avg_confidence) if avg_confidence else None,
        escalation_rate=round(escalation_rate, 2),
        conversations_by_agent=conversations_by_agent,
        conversations_by_intent=conversations_by_intent,
        conversations_by_sentiment=conversations_by_sentiment
    )


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


