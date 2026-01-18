"""
Sentiment analysis service using rule-based approach.
"""
from typing import Tuple


class SentimentService:
    """
    Service for analyzing sentiment of user messages.
    Uses rule-based keyword matching for sentiment classification.
    """
    
    # Positive sentiment indicators with weights
    POSITIVE_WORDS = {
        "excellent": 0.9, "great": 0.8, "good": 0.7, "wonderful": 0.9,
        "amazing": 0.85, "fantastic": 0.85, "love": 0.9, "perfect": 0.9,
        "thank": 0.6, "thanks": 0.6, "appreciate": 0.7, "happy": 0.8,
        "satisfied": 0.75, "pleased": 0.75, "awesome": 0.8, "brilliant": 0.85
    }
    
    # Negative sentiment indicators with weights
    NEGATIVE_WORDS = {
        "terrible": -0.9, "awful": -0.9, "horrible": -0.9, "bad": -0.7,
        "worst": -0.95, "hate": -0.9, "disappointed": -0.8, "frustrated": -0.8,
        "angry": -0.85, "complaint": -0.7, "issue": -0.6, "problem": -0.6,
        "broken": -0.75, "not working": -0.7, "dissatisfied": -0.8, "unhappy": -0.8,
        "refund": -0.5, "cancel": -0.5, "poor": -0.75, "slow": -0.6
    }
    
    # Intensifiers
    INTENSIFIERS = {
        "very": 1.3, "extremely": 1.5, "really": 1.2, "super": 1.2,
        "incredibly": 1.4, "absolutely": 1.3, "totally": 1.2
    }
    
    # Negation words
    NEGATIONS = ["not", "no", "never", "none", "nobody", "nothing", "nowhere"]
    
    def analyze_sentiment(self, message: str) -> Tuple[float, str]:
        """
        Analyze sentiment of a message.
        
        Args:
            message: User's message text
            
        Returns:
            Tuple of (sentiment_score, sentiment_label)
            sentiment_score: Range from -1.0 (very negative) to 1.0 (very positive)
            sentiment_label: "positive", "neutral", or "negative"
        """
        message_lower = message.lower()
        words = message_lower.split()
        
        sentiment_score = 0.0
        word_count = len(words)
        
        if word_count == 0:
            return (0.0, "neutral")
        
        # Check for positive and negative words
        i = 0
        while i < len(words):
            word = words[i]
            multiplier = 1.0
            
            # Check for intensifiers before the word
            if i > 0 and words[i - 1] in self.INTENSIFIERS:
                multiplier = self.INTENSIFIERS[words[i - 1]]
            
            # Check for negations (inverts sentiment)
            has_negation = any(
                words[max(0, i - j - 1)] in self.NEGATIONS
                for j in range(min(3, i + 1))
            )
            
            # Check positive words
            if word in self.POSITIVE_WORDS:
                score = self.POSITIVE_WORDS[word] * multiplier
                if has_negation:
                    score = -abs(score) * 0.7
                sentiment_score += score
            
            # Check negative words
            elif word in self.NEGATIVE_WORDS:
                score = self.NEGATIVE_WORDS[word] * multiplier
                if has_negation:
                    score = abs(score) * 0.7
                sentiment_score += score
            
            i += 1
        
        # Normalize sentiment score to -1.0 to 1.0 range
        # Use logarithmic scaling for better distribution
        normalized_score = max(-1.0, min(1.0, sentiment_score / max(1, word_count * 0.5)))
        
        # Determine sentiment label
        if normalized_score > 0.3:
            sentiment_label = "positive"
        elif normalized_score < -0.3:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"
        
        return (normalized_score, sentiment_label)


sentiment_service = SentimentService()


