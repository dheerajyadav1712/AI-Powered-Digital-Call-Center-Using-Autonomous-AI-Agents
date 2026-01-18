"""
Base agent class for all AI agents in the system.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from app.services.llm_service import llm_service
from app.services.intent_service import intent_service
from app.services.sentiment_service import sentiment_service


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents.
    Provides common functionality for intent detection, sentiment analysis, and response generation.
    """
    
    def __init__(self, agent_name: str, agent_type: str):
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.llm_service = llm_service
        self.intent_service = intent_service
        self.sentiment_service = sentiment_service
    
    @abstractmethod
    def process_message(
        self,
        message: str,
        conversation_history: List[Dict[str, str]],
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Process a customer message and generate a response.
        
        Args:
            message: Customer's message
            conversation_history: Previous messages in the conversation
            context: Additional context information
            
        Returns:
            Dictionary containing response, confidence, intent, sentiment, and metadata
        """
        pass
    
    def analyze_message(self, message: str) -> Dict:
        """
        Analyze a message to extract intent and sentiment.
        
        Args:
            message: Customer's message
            
        Returns:
            Dictionary with intent and sentiment information
        """
        # Detect intent
        intent_name, intent_confidence = self.intent_service.detect_intent(message)
        intent_label = self.intent_service.get_intent_label(intent_name)
        
        # Analyze sentiment
        sentiment_score, sentiment_label = self.sentiment_service.analyze_sentiment(message)
        
        return {
            "intent": intent_name,
            "intent_label": intent_label,
            "intent_confidence": intent_confidence,
            "sentiment_score": sentiment_score,
            "sentiment_label": sentiment_label
        }
    
    def calculate_confidence(
        self,
        intent_confidence: float,
        sentiment_score: float,
        message_length: int,
        context: Optional[Dict] = None
    ) -> float:
        """
        Calculate overall confidence score for the agent's response.
        
        Args:
            intent_confidence: Confidence in intent detection
            sentiment_score: Sentiment score
            message_length: Length of customer message
            context: Additional context
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Base confidence from intent detection
        confidence = intent_confidence
        
        # Adjust based on message clarity (longer messages might be clearer)
        length_factor = min(1.0, message_length / 50)  # Normalize to ~50 chars
        confidence = confidence * 0.7 + (intent_confidence * length_factor) * 0.3
        
        # Adjust based on sentiment clarity
        sentiment_clarity = abs(sentiment_score)
        confidence = confidence * 0.8 + (intent_confidence * sentiment_clarity) * 0.2
        
        # Ensure confidence is in valid range
        return max(0.0, min(1.0, confidence))


