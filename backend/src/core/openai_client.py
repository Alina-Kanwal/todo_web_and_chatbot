"""
Groq client configuration and initialization.
"""

from functools import lru_cache
from groq import Groq
from src.core.config import get_settings

settings = get_settings()


@lru_cache
def get_openai_client() -> Groq:
    """
    Get cached Groq client instance.

    Returns:
        Groq: Configured Groq client

    Raises:
        ValueError: If OPENAI_API_KEY is not configured
    """
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    return Groq(
        api_key=settings.openai_api_key,
    )
