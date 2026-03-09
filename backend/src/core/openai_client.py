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
        ValueError: If GROQ_API_KEY is not configured
    """
    api_key = settings.effective_api_key
    
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    return Groq(
        api_key=api_key,
    )
