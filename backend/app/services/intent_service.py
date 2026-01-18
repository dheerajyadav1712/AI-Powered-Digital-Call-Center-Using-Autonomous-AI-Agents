"""
Intent detection service using rule-based and pattern matching approaches.
"""
import re
from typing import Dict, List, Tuple


class IntentService:
    """
    Service for detecting user intent from messages.
    Uses rule-based pattern matching for reliable intent classification.
    """
    
    # Intent patterns with keywords and confidence mapping
    INTENT_PATTERNS: Dict[str, Dict[str, any]] = {
        "order_inquiry": {
            "keywords": ["order", "purchase", "buy", "product", "item", "cart"],
            "confidence": 0.85
        },
        "refund_request": {
            "keywords": ["refund", "return", "cancel", "money back", "reimburse"],
            "confidence": 0.90
        },
        "tracking_inquiry": {
            "keywords": ["track", "shipping", "delivery", "status", "when", "arrive"],
            "confidence": 0.88
        },
        "technical_support": {
            "keywords": ["problem", "issue", "broken", "not working", "error", "bug", "fix"],
            "confidence": 0.87
        },
        "account_management": {
            "keywords": ["account", "login", "password", "access", "profile", "settings"],
            "confidence": 0.86
        },
        "billing_inquiry": {
            "keywords": ["billing", "payment", "invoice", "charge", "bill", "payment method"],
            "confidence": 0.89
        },
        "complaint": {
            "keywords": ["complaint", "dissatisfied", "unhappy", "bad", "terrible", "horrible"],
            "confidence": 0.92
        },
        "praise": {
            "keywords": ["thank", "thanks", "appreciate", "great", "excellent", "love"],
            "confidence": 0.80
        },
        "greeting": {
            "keywords": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"],
            "confidence": 0.75
        },
        "general_inquiry": {
            "keywords": ["information", "question", "help", "assist", "wondering"],
            "confidence": 0.70
        }
    }
    
    def detect_intent(self, message: str) -> Tuple[str, float]:
        """
        Detect intent from a user message.
        
        Args:
            message: User's message text
            
        Returns:
            Tuple of (intent_name, confidence_score)
        """
        message_lower = message.lower()
        intent_scores = {}
        
        # Score each intent pattern
        for intent_name, intent_data in self.INTENT_PATTERNS.items():
            keyword_matches = sum(
                1 for keyword in intent_data["keywords"]
                if keyword in message_lower
            )
            
            if keyword_matches > 0:
                # Calculate confidence based on matches and base confidence
                match_ratio = min(keyword_matches / len(intent_data["keywords"]), 1.0)
                confidence = intent_data["confidence"] * (0.7 + 0.3 * match_ratio)
                intent_scores[intent_name] = confidence
        
        if intent_scores:
            # Return intent with highest confidence
            best_intent = max(intent_scores.items(), key=lambda x: x[1])
            return best_intent
        
        # Default to general inquiry if no pattern matches
        return ("general_inquiry", 0.65)
    
    def get_intent_label(self, intent_name: str) -> str:
        """
        Get human-readable label for intent.
        """
        intent_labels = {
            "order_inquiry": "Order Inquiry",
            "refund_request": "Refund Request",
            "tracking_inquiry": "Tracking Inquiry",
            "technical_support": "Technical Support",
            "account_management": "Account Management",
            "billing_inquiry": "Billing Inquiry",
            "complaint": "Complaint",
            "praise": "Praise/Thank You",
            "greeting": "Greeting",
            "general_inquiry": "General Inquiry"
        }
        return intent_labels.get(intent_name, "Unknown")


intent_service = IntentService()


