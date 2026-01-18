"""
Escalation AI Agent - Manages escalation workflow and coordinates with human agents.
"""
from typing import Dict, List, Optional
from datetime import datetime

from app.agents.base_agent import BaseAgent
from app.services.ticket_service import ticket_service


class EscalationAgent(BaseAgent):
    """
    Escalation Agent manages the escalation process and coordinates handoff to human agents.
    Acts as an orchestrator for escalation workflows.
    """
    
    def __init__(self):
        super().__init__("Escalation Agent", "escalation")
    
    def process_message(
        self,
        message: str,
        conversation_history: List[Dict[str, str]] = None,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Process message during escalation workflow.
        
        Args:
            message: Customer's message
            conversation_history: Conversation history
            context: Escalation context
            
        Returns:
            Response dictionary with escalation information
        """
        if conversation_history is None:
            conversation_history = []
        
        # Analyze message
        analysis = self.analyze_message(message)
        
        # Escalation agent prepares context for human agent
        escalation_summary = self._generate_escalation_summary(
            conversation_history=conversation_history,
            context=context
        )
        
        # Response during escalation (before human takeover)
        response = (
            "I understand this requires specialized attention. "
            "I'm connecting you with one of our human agents who can better assist you. "
            "Please hold while I transfer your case. "
            "They have access to our conversation history and will be with you shortly."
        )
        
        # Escalation agent confidence is based on successful handoff preparation
        confidence = 0.95  # High confidence in handoff process
        
        return {
            "agent_type": self.agent_type,
            "agent_name": self.agent_name,
            "response": response,
            "confidence": confidence,
            "intent": analysis["intent"],
            "intent_label": analysis["intent_label"],
            "sentiment_score": analysis["sentiment_score"],
            "sentiment_label": analysis["sentiment_label"],
            "needs_escalation": False,  # Already escalated
            "escalation_summary": escalation_summary,
            "human_handoff": True
        }
    
    def _generate_escalation_summary(
        self,
        conversation_history: List[Dict[str, str]],
        context: Optional[Dict] = None
    ) -> str:
        """
        Generate summary of conversation for human agent handoff.
        
        Args:
            conversation_history: Full conversation history
            context: Escalation context
            
        Returns:
            Summary string for human agent
        """
        summary_parts = []
        
        # Add escalation reason
        if context and context.get("escalation_reason"):
            summary_parts.append(f"Escalation Reason: {context['escalation_reason']}")
        
        # Add key messages
        customer_messages = [
            msg.get("content", "") for msg in conversation_history
            if msg.get("role") == "customer"
        ]
        
        if customer_messages:
            summary_parts.append(f"Customer Messages: {len(customer_messages)}")
            summary_parts.append(f"Latest: {customer_messages[-1][:200]}")
        
        # Add detected intent and sentiment
        if context:
            if context.get("intent"):
                summary_parts.append(f"Detected Intent: {context.get('intent_label', context.get('intent'))}")
            if context.get("sentiment_label"):
                summary_parts.append(f"Sentiment: {context.get('sentiment_label')}")
        
        return " | ".join(summary_parts) if summary_parts else "Escalation requested"
    
    def suggest_ticket_creation(
        self,
        message: str,
        conversation_history: List[Dict[str, str]] = None,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Suggest ticket creation when agent cannot handle the query.
        
        Args:
            message: Customer's message
            conversation_history: Conversation history
            context: Additional context
            
        Returns:
            Response dictionary suggesting ticket creation
        """
        analysis = self.analyze_message(message)
        message_lower = message.lower()
        
        # Determine category based on keywords
        category = self._detect_ticket_category(message_lower, analysis)
        
        # Build response suggesting ticket creation
        response = (
            f"I understand this requires specialized attention. Based on your issue, "
            f"this would be best handled by the {category} team. Let me create a ticket for you.\n\n"
            f"Please provide a detailed description of your problem, and I'll create a ticket "
            f"with the category: {category}.\n\n"
            f"Once you provide the description, I'll generate a ticket number that you can track."
        )
        
        return {
            "agent_type": self.agent_type,
            "agent_name": self.agent_name,
            "response": response,
            "confidence": 0.90,
            "intent": analysis["intent"],
            "intent_label": analysis["intent_label"],
            "sentiment_score": analysis["sentiment_score"],
            "sentiment_label": analysis["sentiment_label"],
            "needs_escalation": False,
            "suggest_ticket": True,
            "suggested_category": category
        }
    
    def _detect_ticket_category(self, message_lower: str, analysis: Dict) -> str:
        """
        Detect appropriate ticket category based on message content.
        
        Args:
            message_lower: Lowercase message
            analysis: Message analysis
            
        Returns:
            Ticket category string
        """
        # Security-related keywords
        if any(word in message_lower for word in ["security", "breach", "hack", "unauthorized", 
                                                   "attack", "virus", "malware", "phishing", 
                                                   "access violation", "data leak"]):
            return "IS Security"
        
        # Proxy/Network keywords
        if any(word in message_lower for word in ["proxy", "vpn", "network", "connection", 
                                                   "internet", "firewall", "dns"]):
            return "Proxy"
        
        # Configuration keywords
        if any(word in message_lower for word in ["configure", "configuration", "setup", 
                                                   "settings", "config", "change", "modify"]):
            return "Configuration and Queries"
        
        # Internal IT keywords
        if any(word in message_lower for word in ["server", "infrastructure", "system", 
                                                   "database", "backup", "maintenance"]):
            return "Internal IT"
        
        # Default to GHD (General Help Desk)
        return "GHD"
    
    def create_ticket_response(
        self,
        description: str,
        category: str,
        ticket_number: str
    ) -> str:
        """
        Generate response after ticket creation.
        
        Args:
            description: Problem description
            category: Ticket category
            ticket_number: Generated ticket number
            
        Returns:
            Response string with ticket information
        """
        return (
            f"Thank you for providing the details! I've created a ticket for you.\n\n"
            f"📋 **Ticket Details:**\n"
            f"• **Ticket Number:** {ticket_number}\n"
            f"• **Category:** {category}\n"
            f"• **Status:** Open\n"
            f"• **Description:** {description[:100]}...\n\n"
            f"✅ Your ticket has been submitted and will be tracked. "
            f"You can use this ticket number to track the status of your request.\n\n"
            f"Ticket No: **{ticket_number}**\n\n"
            f"Is there anything else I can help you with?"
        )
    
    def simulate_human_response(
        self,
        message: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict:
        """
        Simulate a human agent response (for demo purposes).
        In production, this would interface with actual human agent systems.
        
        Args:
            message: Customer's message
            conversation_history: Conversation history
            
        Returns:
            Simulated human agent response
        """
        # In a real system, this would wait for actual human agent input
        # For demo, we simulate with a more personal response
        
        analysis = self.analyze_message(message)
        
        # Simulated human response (more personalized and empathetic)
        human_responses = {
            "complaint": (
                "I sincerely apologize for the inconvenience you've experienced. "
                "I understand how frustrating this must be. Let me personally look into this "
                "and ensure we resolve it to your satisfaction. Could you provide me with "
                "a few more details so I can assist you better?"
            ),
            "refund_request": (
                "I completely understand your situation regarding the refund. "
                "I'm here to help you get this sorted out quickly. Let me check your "
                "account and process this for you right away. Could you confirm your "
                "order number or transaction ID?"
            ),
            "technical_support": (
                "I understand you're experiencing technical difficulties. "
                "Let me help you troubleshoot this step by step. I have access to our "
                "technical resources and can guide you through resolving this issue. "
                "What specific error messages or symptoms are you seeing?"
            )
        }
        
        intent = analysis["intent"]
        response = human_responses.get(
            intent,
            "Thank you for your patience. I'm reviewing your case now and will provide "
            "you with a resolution shortly. How can I best assist you today?"
        )
        
        return {
            "agent_type": "human",
            "agent_name": "Human Agent",
            "response": response,
            "confidence": 0.98,  # High confidence from human agent
            "intent": analysis["intent"],
            "intent_label": analysis["intent_label"],
            "sentiment_score": analysis["sentiment_score"],
            "sentiment_label": analysis["sentiment_label"],
            "needs_escalation": False,
            "human_agent": True
        }


escalation_agent = EscalationAgent()

