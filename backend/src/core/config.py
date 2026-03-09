"""
Backend configuration module.
Loads environment variables and provides type-safe configuration.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

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

    # Groq AI (for chatbot) - supports both GROQ_API_KEY and OPENAI_API_KEY
    groq_api_key: str = ""
    openai_api_key: str = ""  # Alias for GROQ_API_KEY
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.7

    @property
    def effective_api_key(self) -> str:
        """Get effective API key (GROQ_API_KEY takes precedence)."""
        return self.groq_api_key or self.openai_api_key

    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse allowed origins from comma-separated string."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Settings: Application configuration
    """
    return Settings()
