"""
Backend configuration module.
Loads environment variables and provides type-safe configuration.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str
    db_pool_size: int = 5
    db_max_overflow: int = 10
    
    # Authentication
    better_auth_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 10080  # 7 days
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"
    
    # Application
    app_name: str = "Hackathon Todo API"
    debug: bool = False

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.7
    
    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse allowed origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application configuration
    """
    return Settings()
