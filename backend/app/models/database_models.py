"""
Database models for the AI Digital Call Center application.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.core.database import Base


class Conversation(Base):
    """
    Model representing a customer conversation session.
    """
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    customer_id = Column(String(100), index=True)
    channel = Column(String(50), default="chat")  # chat, voice, email, messaging
    status = Column(String(50), default="active")  # active, resolved, escalated, closed
    started_at = Column(DateTime, default=func.now())
    ended_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    escalated_at = Column(DateTime, nullable=True)
    primary_agent_handled = Column(Boolean, default=True)
    supervisor_agent_handled = Column(Boolean, default=False)
    human_agent_handled = Column(Boolean, default=False)
    resolution_time_seconds = Column(Integer, nullable=True)
    
    # Relationships
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    feedback = relationship("Feedback", back_populates="conversation", uselist=False)


class Message(Base):
    """
    Model representing individual messages in a conversation.
    """
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(50), nullable=False)  # customer, primary_agent, supervisor_agent, escalation_agent, human_agent
    content = Column(Text, nullable=False)
    intent = Column(String(100), nullable=True)
    sentiment_score = Column(Float, nullable=True)  # Range: -1.0 to 1.0
    sentiment_label = Column(String(50), nullable=True)  # positive, neutral, negative
    confidence_score = Column(Float, nullable=True)  # Range: 0.0 to 1.0
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class Feedback(Base):
    """
    Model representing customer satisfaction feedback (CSAT).
    """
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), unique=True, nullable=False)
    csat_score = Column(Integer, nullable=False)  # 1-5 scale
    feedback_text = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="feedback")


class AgentMetric(Base):
    """
    Model for storing agent performance metrics.
    """
    __tablename__ = "agent_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_type = Column(String(50), nullable=False)  # primary, supervisor, escalation, human
    date = Column(DateTime, default=func.now())
    conversations_handled = Column(Integer, default=0)
    average_confidence = Column(Float, nullable=True)
    average_response_time_seconds = Column(Float, nullable=True)
    escalation_count = Column(Integer, default=0)
    resolution_rate = Column(Float, nullable=True)


class Ticket(Base):
    """
    Model representing support tickets.
    """
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String(50), unique=True, index=True, nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)
    customer_id = Column(String(100), index=True)
    category = Column(String(50), nullable=False)  # GHD, Internal IT, IS Security, Proxy, Configuration and Queries
    title = Column(String(200), nullable=True)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="open")  # open, in_progress, resolved, closed
    priority = Column(String(20), default="medium")  # low, medium, high, critical
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationships
    conversation = relationship("Conversation")

