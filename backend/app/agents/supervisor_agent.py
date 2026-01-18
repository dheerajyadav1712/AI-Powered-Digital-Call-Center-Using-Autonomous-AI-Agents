"""
Supervisor AI Agent - Handles complex queries escalated from Primary Agent.
"""
from typing import Dict, List, Optional
import random

from app.agents.base_agent import BaseAgent
from app.core.config import settings


class SupervisorAgent(BaseAgent):
    """
    Supervisor AI Agent handles escalated queries from Primary Agent.
    Has access to more context and can make decisions about further escalation.
    """
    
    def __init__(self):
        super().__init__("Supervisor Agent", "supervisor")
        self.confidence_threshold = settings.SUPERVISOR_AGENT_CONFIDENCE_THRESHOLD
    
    def process_message(
        self,
        message: str,
        conversation_history: List[Dict[str, str]] = None,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Process escalated message and generate response.
        
        Args:
            message: Customer's message
            conversation_history: Full conversation history including primary agent interactions
            context: Additional context including escalation reason
            
        Returns:
            Response dictionary
        """
        if conversation_history is None:
            conversation_history = []
        
        # Analyze message with supervisor-level analysis
        analysis = self.analyze_message(message)
        
        # Prepare enhanced context for LLM (supervisor has access to more context)
        llm_context = []
        for msg in conversation_history[-10:]:  # Last 10 messages for better context
            role = "assistant" if msg.get("role") != "customer" else "user"
            llm_context.append({"role": role, "content": msg.get("content", "")})
        
        # Add escalation context to prompt
        escalation_reason = context.get("escalation_reason", "") if context else ""
        enhanced_prompt = message
        if escalation_reason:
            enhanced_prompt = f"[Escalated: {escalation_reason}] {message}"
        
        # Generate response using LLM with enhanced context
        response = self.llm_service.generate_response(
            prompt=enhanced_prompt,
            context=llm_context,
            max_tokens=250  # Longer responses for complex queries
        )
        
        # Supervisor typically has higher confidence due to more context
        base_confidence = self.calculate_confidence(
            intent_confidence=analysis["intent_confidence"],
            sentiment_score=analysis["sentiment_score"],
            message_length=len(message),
            context=context
        )
        
        # Supervisor agent gets boost from having full conversation context
        confidence = min(1.0, base_confidence * 1.1)
        confidence = max(0.0, min(1.0, confidence + random.uniform(-0.03, 0.03)))
        
        # Determine if further escalation to human is needed
        needs_human_escalation = self._should_escalate_to_human(
            message=message,
            confidence=confidence,
            sentiment=analysis["sentiment_label"],
            intent=analysis["intent"],
            context=context
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
            "needs_escalation": needs_human_escalation,
            "escalation_reason": self._get_human_escalation_reason(needs_human_escalation, confidence, message) if needs_human_escalation else None
        }
    
    def _should_escalate_to_human(
        self,
        message: str,
        confidence: float,
        sentiment: str,
        intent: str,
        context: Optional[Dict] = None
    ) -> bool:
        """
        Determine if query should be escalated to human agent.
        
        Args:
            message: Customer's message
            confidence: Supervisor agent's confidence
            sentiment: Sentiment label
            intent: Detected intent
            context: Additional context
            
        Returns:
            True if human escalation is needed
        """
        message_lower = message.lower()
        
        # Escalate to human if confidence is still below supervisor threshold
        if confidence < settings.ESCALATION_CONFIDENCE_THRESHOLD:
            return True
        
        # Escalate to human for serious complaints
        if intent == "complaint" and sentiment == "negative" and confidence < 0.80:
            return True
        
        # Escalate to human for explicit requests
        human_keywords = ["human", "person", "manager", "supervisor", "real person", "talk to someone"]
        if any(keyword in message_lower for keyword in human_keywords):
            return True
        
        # Escalate after multiple attempts (check context)
        if context and context.get("message_count", 0) > settings.MAX_AUTO_RESPONSES:
            return True
        
        return False
    
    def _get_human_escalation_reason(
        self,
        needs_escalation: bool,
        confidence: float,
        message: str
    ) -> Optional[str]:
        """
        Get reason for human escalation.
        
        Args:
            needs_escalation: Whether human escalation is needed
            confidence: Agent confidence
            message: Customer message
            
        Returns:
            Human escalation reason string
        """
        if not needs_escalation:
            return None
        
        message_lower = message.lower()
        
        if "human" in message_lower or "person" in message_lower or "manager" in message_lower:
            return "Explicit request for human agent"
        
        if confidence < settings.ESCALATION_CONFIDENCE_THRESHOLD:
            return "Complex query requiring human judgment"
        
        return "Escalated to human agent for resolution"


supervisor_agent = SupervisorAgent()


