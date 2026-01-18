"""
Conversation service for managing conversation flow and agent interactions.
"""
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import uuid

from app.models.database_models import Conversation, Message
from app.agents.primary_agent import primary_agent
from app.agents.supervisor_agent import supervisor_agent
from app.agents.escalation_agent import escalation_agent


class ConversationService:
    """
    Service for managing conversations and orchestrating agent interactions.
    """
    
    def __init__(self):
        self.primary_agent = primary_agent
        self.supervisor_agent = supervisor_agent
        self.escalation_agent = escalation_agent
    
    async def process_message(
        self,
        message: str,
        session_id: Optional[str],
        customer_id: Optional[str],
        db: Session
    ) -> Dict:
        """
        Process a customer message through the agent system.
        
        Args:
            message: Customer's message
            session_id: Existing session ID or None for new conversation
            customer_id: Customer identifier
            db: Database session
            
        Returns:
            Dictionary with response and metadata
        """
        # Get or create conversation
        conversation = self._get_or_create_conversation(
            session_id=session_id,
            customer_id=customer_id,
            db=db
        )
        
        # Save customer message
        customer_message = Message(
            conversation_id=conversation.id,
            role="customer",
            content=message,
            created_at=datetime.now()
        )
        db.add(customer_message)
        db.commit()
        
        # Get conversation history
        conversation_history = self._get_conversation_history(conversation.id, db)
        
        # Determine which agent should handle this message
        agent_response = self._route_to_agent(
            message=message,
            conversation=conversation,
            conversation_history=conversation_history,
            db=db
        )
        
        # Save agent response
        agent_message = Message(
            conversation_id=conversation.id,
            role=agent_response["agent_type"],
            content=agent_response["response"],
            intent=agent_response["intent"],
            sentiment_score=agent_response["sentiment_score"],
            sentiment_label=agent_response["sentiment_label"],
            confidence_score=agent_response["confidence"],
            created_at=datetime.now()
        )
        db.add(agent_message)
        
        # Update conversation status based on agent response
        self._update_conversation_status(conversation, agent_response, db)
        
        db.commit()
        db.refresh(conversation)
        
        return {
            "session_id": conversation.session_id,
            "response": agent_response["response"],
            "agent_type": agent_response["agent_type"],
            "agent_name": agent_response["agent_name"],
            "confidence": agent_response["confidence"],
            "intent": agent_response["intent"],
            "intent_label": agent_response.get("intent_label", agent_response["intent"]),
            "sentiment_score": agent_response["sentiment_score"],
            "sentiment_label": agent_response["sentiment_label"],
            "needs_escalation": agent_response.get("needs_escalation", False),
            "escalation_reason": agent_response.get("escalation_reason"),
            "timestamp": datetime.now()
        }
    
    def _get_or_create_conversation(
        self,
        session_id: Optional[str],
        customer_id: Optional[str],
        db: Session
    ) -> Conversation:
        """
        Get existing conversation or create new one.
        
        Args:
            session_id: Session ID
            customer_id: Customer ID
            db: Database session
            
        Returns:
            Conversation object
        """
        if session_id:
            conversation = db.query(Conversation).filter(
                Conversation.session_id == session_id
            ).first()
            
            if conversation:
                return conversation
        
        # Create new conversation
        new_session_id = session_id or str(uuid.uuid4())
        conversation = Conversation(
            session_id=new_session_id,
            customer_id=customer_id,
            channel="chat",
            status="active",
            started_at=datetime.now(),
            primary_agent_handled=False,
            supervisor_agent_handled=False,
            human_agent_handled=False
        )
        
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        return conversation
    
    def _get_conversation_history(self, conversation_id: int, db: Session) -> List[Dict]:
        """
        Get conversation history as list of message dictionaries.
        
        Args:
            conversation_id: Conversation ID
            db: Database session
            
        Returns:
            List of message dictionaries
        """
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    
    def _route_to_agent(
        self,
        message: str,
        conversation: Conversation,
        conversation_history: List[Dict],
        db: Session
    ) -> Dict:
        """
        Route message to appropriate agent based on conversation state.
        
        Args:
            message: Customer message
            conversation: Conversation object
            conversation_history: Conversation history
            db: Database session
            
        Returns:
            Agent response dictionary
        """
        # If already escalated to human, use escalation agent for handoff
        if conversation.human_agent_handled:
            return self.escalation_agent.simulate_human_response(message, conversation_history)
        
        # If already escalated to supervisor, try supervisor agent first
        if conversation.supervisor_agent_handled:
            context = {
                "message_count": len(conversation_history),
                "escalation_reason": "Previously escalated"
            }
            supervisor_response = self.supervisor_agent.process_message(
                message=message,
                conversation_history=conversation_history,
                context=context
            )
            
            # If supervisor also needs escalation, go to human
            if supervisor_response.get("needs_escalation"):
                return self.escalation_agent.process_message(
                    message=message,
                    conversation_history=conversation_history,
                    context={"escalation_reason": supervisor_response.get("escalation_reason")}
                )
            
            return supervisor_response
        
        # Start with primary agent
        primary_response = self.primary_agent.process_message(
            message=message,
            conversation_history=conversation_history
        )
        
        # If primary agent needs escalation, try supervisor
        if primary_response.get("needs_escalation"):
            context = {
                "message_count": len(conversation_history),
                "escalation_reason": primary_response.get("escalation_reason"),
                "intent": primary_response.get("intent"),
                "sentiment_label": primary_response.get("sentiment_label")
            }
            supervisor_response = self.supervisor_agent.process_message(
                message=message,
                conversation_history=conversation_history,
                context=context
            )
            
            # If supervisor also needs escalation, go to human
            if supervisor_response.get("needs_escalation"):
                return self.escalation_agent.process_message(
                    message=message,
                    conversation_history=conversation_history,
                    context={"escalation_reason": supervisor_response.get("escalation_reason")}
                )
            
            return supervisor_response
        
        # Primary agent can handle it
        return primary_response
    
    def _update_conversation_status(
        self,
        conversation: Conversation,
        agent_response: Dict,
        db: Session
    ):
        """
        Update conversation status based on agent response.
        
        Args:
            conversation: Conversation object
            agent_response: Agent response dictionary
            db: Database session
        """
        agent_type = agent_response["agent_type"]
        
        if agent_type == "primary":
            conversation.primary_agent_handled = True
        
        elif agent_type == "supervisor":
            conversation.primary_agent_handled = True
            conversation.supervisor_agent_handled = True
        
        elif agent_type == "escalation" or agent_type == "human":
            conversation.primary_agent_handled = True
            conversation.supervisor_agent_handled = True
            conversation.human_agent_handled = True
            conversation.escalated_at = datetime.now()
            conversation.status = "escalated"
        
        # Check if conversation should be marked as resolved
        if not agent_response.get("needs_escalation") and agent_type != "escalation":
            # In a real system, we'd have logic to determine resolution
            # For now, we'll keep it active unless explicitly resolved
            pass


conversation_service = ConversationService()


