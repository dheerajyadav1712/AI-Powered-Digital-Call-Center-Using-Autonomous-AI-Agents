"""
Configuration settings for the AI Digital Call Center application.
"""
import os
from typing import Optional

class Settings:
    """Application settings and configuration."""
    
    # Application
    APP_NAME: str = "AI Digital Call Center"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./database/call_center.db"
    )
    
    # AI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "mock-key-for-local-dev")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    USE_MOCK_LLM: bool = os.getenv("USE_MOCK_LLM", "True").lower() == "true"
    
    # Agent Configuration
    PRIMARY_AGENT_CONFIDENCE_THRESHOLD: float = 0.70
    SUPERVISOR_AGENT_CONFIDENCE_THRESHOLD: float = 0.85
    ESCALATION_CONFIDENCE_THRESHOLD: float = 0.60
    
    # Escalation Settings
    MAX_AUTO_RESPONSES: int = 5
    ESCALATION_TRIGGER_KEYWORDS: list = [
        "manager", "supervisor", "human", "person", "complaint", 
        "refund", "cancel", "dispute", "legal"
    ]
    
    # Sentiment Thresholds
    NEGATIVE_SENTIMENT_THRESHOLD: float = -0.3
    POSITIVE_SENTIMENT_THRESHOLD: float = 0.3
    
    # Database Path
    DATABASE_DIR: str = "./database"
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]


settings = Settings()


