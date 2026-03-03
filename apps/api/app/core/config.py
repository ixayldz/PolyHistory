from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "PolyHistory API"
    DEBUG: bool = False
    VERSION: str = "2.0.0"
    SECRET_KEY: str = "supersecretkey"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/polyhistory"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    # AI Model API Keys
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Model Settings
    MODEL_TIMEOUT_SECONDS: int = 30
    MAX_CONCURRENT_MODELS: int = 3
    
    # Consensus Settings
    CONSENSUS_SIMILARITY_THRESHOLD: float = 0.85
    MIN_MODELS_FOR_CONSENSUS: int = 1  # Lowered: graceful degradation handles partial responses
    CONSENSUS_AGREEMENT_WEIGHT: float = 0.4
    CONSENSUS_EVIDENCE_WEIGHT: float = 0.6
    
    # Evidence Settings
    MAX_EVIDENCE_PER_CASE: int = 100
    SNIPPET_MAX_LENGTH: int = 1000
    
    # Balance Protocol
    MBR_PENALTY_PERCENTAGE: int = 20
    HIGH_RISK_CONFIDENCE_CAP: float = 0.6

    # Free Tier Limits
    FREE_TIER_MULTI_MODEL_LIMIT: int = 1
    FREE_TIER_SINGLE_MODEL_LIMIT: int = 4

    # Celery
    CELERY_TASK_ALWAYS_EAGER: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated configuration."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
