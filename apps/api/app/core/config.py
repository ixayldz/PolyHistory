from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "PolyHistory API"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    SECRET_KEY: str = "supersecretkey"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/polyhistory"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"
    
    # AI Model API Keys
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Model Settings
    MODEL_TIMEOUT_SECONDS: int = 30
    MAX_CONCURRENT_MODELS: int = 3
    
    # Consensus Settings
    CONSENSUS_SIMILARITY_THRESHOLD: float = 0.85
    MIN_MODELS_FOR_CONSENSUS: int = 2
    
    # Evidence Settings
    MAX_EVIDENCE_PER_CASE: int = 100
    SNIPPET_MAX_LENGTH: int = 1000
    
    # Balance Protocol
    MBR_PENALTY_PERCENTAGE: int = 20
    HIGH_RISK_CONFIDENCE_CAP: float = 0.6
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
