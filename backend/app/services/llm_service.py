"""
LLM service for handling AI model interactions.
Supports both real OpenAI API and mock implementation for local development.
"""
import json
import random
from typing import Dict, List, Optional

from app.core.config import settings


class LLMService:
    """
    Service for interacting with LLM models.
    Provides mock implementation for local development without API keys.
    """
    
    def __init__(self):
        self.use_mock = settings.USE_MOCK_LLM or not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "mock-key-for-local-dev"
    
    def generate_response(
        self,
        prompt: str,
        context: Optional[List[Dict[str, str]]] = None,
        max_tokens: int = 200,
        temperature: float = 0.7
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user's message or prompt
            context: Conversation history as list of {"role": str, "content": str}
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated response text
        """
        if self.use_mock:
            return self._mock_generate_response(prompt, context)
        else:
            return self._openai_generate_response(prompt, context, max_tokens, temperature)
    
    def _mock_generate_response(
        self,
        prompt: str,
        context: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Mock LLM response generator for local development.
        Provides realistic responses based on intent patterns.
        """
        prompt_lower = prompt.lower().strip()
        
        # Handle empty or very short messages
        if len(prompt_lower) <= 2:
            return "Hello! I'm here to help you. How can I assist you today?"
        
        # Check greetings FIRST (most common initial message)
        greeting_words = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "namaste", "hey there"]
        if any(word in prompt_lower for word in greeting_words):
            greetings = [
                "Hello! 👋 Thank you for contacting our support team. I'm an AI assistant ready to help you. How can I assist you today?",
                "Hi there! Welcome! I'm here to assist you with any questions or concerns you might have. What can I help you with?",
                "Hello! Great to hear from you! I'm ready to help. What would you like assistance with today?",
                "Hey! 👋 Thanks for reaching out. I'm your AI support agent, and I'm here to help. How can I assist you?"
            ]
            return random.choice(greetings)
        
        # Intent-based response mapping
        if any(word in prompt_lower for word in ["order", "purchase", "buy", "product"]):
            return "I'd be happy to help you with your order inquiry. Could you please provide your order number or details about the product you're interested in?"
        
        elif any(word in prompt_lower for word in ["refund", "return", "cancel"]):
            return "I understand you'd like to process a refund or return. Let me check our return policy for you. Generally, items can be returned within 30 days of purchase with a receipt."
        
        elif any(word in prompt_lower for word in ["track", "shipping", "delivery", "status"]):
            return "I can help you track your order. Please provide your tracking number or order ID, and I'll look up the current shipping status for you."
        
        elif any(word in prompt_lower for word in ["problem", "issue", "broken", "not working", "error", "failed"]):
            return "I'm sorry to hear you're experiencing an issue. Let me help troubleshoot this. Could you please describe the problem in more detail? If this is a complex technical issue, I can create a ticket for proper tracking."
        
        # Security-related issues
        elif any(word in prompt_lower for word in ["security", "hack", "breach", "unauthorized", "attack", "virus"]):
            return "I understand this is a security-related concern. This requires immediate attention from our IS Security team. Let me create a ticket for you so this can be tracked and resolved promptly. Please provide a detailed description of the security issue."
        
        # Network/Proxy issues
        elif any(word in prompt_lower for word in ["proxy", "vpn", "network", "connection", "internet", "firewall"]):
            return "I see you're having network/connectivity issues. This would be best handled by our Proxy/Network team. Let me create a ticket for tracking. Could you please describe the connectivity problem in detail?"
        
        # Configuration issues
        elif any(word in prompt_lower for word in ["configure", "configuration", "setup", "settings", "config"]):
            return "I understand you need help with configuration. This falls under Configuration and Queries. Let me create a ticket for you. Please provide details about what you're trying to configure."
        
        elif any(word in prompt_lower for word in ["account", "login", "password", "access"]):
            return "I can assist you with account-related matters. For security purposes, please provide your registered email address, and I'll guide you through the next steps."
        
        elif any(word in prompt_lower for word in ["billing", "payment", "invoice", "charge"]):
            return "I can help you with billing inquiries. Please share your account number or invoice reference, and I'll pull up the details for you."
        
        elif any(word in prompt_lower for word in ["complaint", "dissatisfied", "unhappy", "bad"]):
            return "I'm sorry to hear about your negative experience. Your satisfaction is important to us. Let me see how we can make this right. Could you share more details?"
        
        elif any(word in prompt_lower for word in ["thank", "thanks", "appreciate"]):
            return "You're very welcome! I'm glad I could help. Is there anything else you need assistance with today?"
        
        else:
            # Generic helpful response - more natural AI agent style
            responses = [
                "I understand. Let me help you with that. Could you provide a bit more information about what you need?",
                "Thank you for reaching out! I'm looking into this for you. Could you share some additional details so I can assist you better?",
                "I'd be happy to help! To provide the best assistance, could you elaborate a bit more on your request?",
                "Let me help you with that. What specific information or service are you looking for? Feel free to share more details.",
                "I'm here to assist you! Could you provide more context about your question so I can help you better?"
            ]
            return random.choice(responses)
    
    def _openai_generate_response(
        self,
        prompt: str,
        context: Optional[List[Dict[str, str]]] = None,
        max_tokens: int = 200,
        temperature: float = 0.7
    ) -> str:
        """
        Real OpenAI API implementation.
        This would use the actual OpenAI SDK in production.
        """
        try:
            import openai
            
            messages = context or []
            messages.append({"role": "user", "content": prompt})
            
            response = openai.ChatCompletion.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            # Fallback to mock if API fails
            return self._mock_generate_response(prompt, context)


llm_service = LLMService()

