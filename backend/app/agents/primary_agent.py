"""
Primary AI Agent - First line of support for customer inquiries.
"""
from typing import Dict, List, Optional
import random

from app.agents.base_agent import BaseAgent
from app.core.config import settings


class PrimaryAgent(BaseAgent):
    """
    Primary AI Agent handles initial customer interactions.
    Attempts to resolve queries independently with high confidence.
    """
    
    def __init__(self):
        super().__init__("Primary Agent", "primary")
        self.confidence_threshold = settings.PRIMARY_AGENT_CONFIDENCE_THRESHOLD
    
    def process_message(
        self,
        message: str,
        conversation_history: List[Dict[str, str]] = None,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Process customer message and generate response.
        
        Args:
            message: Customer's message
            conversation_history: Previous conversation messages
            context: Additional context
            
        Returns:
            Response dictionary with agent information, response, confidence, etc.
        """
        if conversation_history is None:
            conversation_history = []
        
        # Analyze message
        analysis = self.analyze_message(message)
        
        # Prepare conversation context for LLM
        llm_context = []
        for msg in conversation_history[-5:]:  # Last 5 messages for context
            role = "assistant" if msg.get("role") != "customer" else "user"
            llm_context.append({"role": role, "content": msg.get("content", "")})
        
        # Generate response using LLM
        response = self.llm_service.generate_response(
            prompt=message,
            context=llm_context,
            max_tokens=200
        )
        
        # Calculate confidence
        confidence = self.calculate_confidence(
            intent_confidence=analysis["intent_confidence"],
            sentiment_score=analysis["sentiment_score"],
            message_length=len(message),
            context=context
        )
        
        # Ensure greetings and simple queries have high confidence
        if analysis["intent"] in ["greeting", "praise"]:
            confidence = max(confidence, 0.80)  # Greetings should have at least 80% confidence
        
        # Add slight randomness to confidence for realism
        confidence = max(0.0, min(1.0, confidence + random.uniform(-0.03, 0.03)))
        
        # Determine if escalation is needed
        needs_escalation = self._should_escalate(
            message=message,
            confidence=confidence,
            sentiment=analysis["sentiment_label"],
            intent=analysis["intent"]
        )
        
        return {
            "agent_type": self.agent_type,
            "agent_name": self.agent_name,
            "response": response,
            "confidence": confidence,
            "intent": analysis["intent"],
            "intent_label": analysis["intent_label"],
            "sentiment_score": analysis["sentiment_score"],
            "sentiment_label": analysis["sentiment_label"],
            "needs_escalation": needs_escalation,
            "escalation_reason": self._get_escalation_reason(needs_escalation, confidence, message) if needs_escalation else None
        }
    
    def _should_escalate(
        self,
        message: str,
        confidence: float,
        sentiment: str,
        intent: str
    ) -> bool:
        """
        Determine if message should be escalated to supervisor or human agent.
        
        Args:
            message: Customer's message
            confidence: Agent's confidence in response
            sentiment: Sentiment label
            intent: Detected intent
            
        Returns:
            True if escalation is needed, False otherwise
        """
        message_lower = message.lower().strip()
        
        # NEVER escalate greetings - these are simple interactions
        greeting_words = ["hello", "hi", "hey", "greetings", "good morning", 
                         "good afternoon", "good evening", "namaste", "hey there"]
        if any(word in message_lower for word in greeting_words) and len(message_lower) <= 15:
            return False
        
        # NEVER escalate praise/thank you messages
        if intent in ["praise", "greeting"]:
            return False
        
        # Escalate if confidence is below threshold (but not for greetings/praise)
        if confidence < self.confidence_threshold:
            return True
        
        # Escalate for complaints with negative sentiment
        if intent == "complaint" and sentiment == "negative":
            return True
        
        # Escalate if escalation keywords are present
        if any(keyword in message_lower for keyword in settings.ESCALATION_TRIGGER_KEYWORDS):
            return True
        
        # Escalate for refund requests with negative sentiment (higher risk)
        if intent == "refund_request" and sentiment == "negative" and confidence < 0.75:
            return True
        
        return False
    
    def _get_escalation_reason(
        self,
        needs_escalation: bool,
        confidence: float,
        message: str
    ) -> Optional[str]:
        """
        Get reason for escalation.
        
        Args:
            needs_escalation: Whether escalation is needed
            confidence: Agent confidence
            message: Customer message
            
        Returns:
            Escalation reason string
        """
        if not needs_escalation:
            return None
        
        message_lower = message.lower()
        
        if confidence < self.confidence_threshold:
            return "Low confidence in response"
        
        if any(keyword in message_lower for keyword in settings.ESCALATION_TRIGGER_KEYWORDS):
            return "Escalation keyword detected"
        
        return "Complex query requiring specialist attention"


primary_agent = PrimaryAgent()

