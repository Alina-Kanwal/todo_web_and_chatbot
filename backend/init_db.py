"""
Quick database initialization script.
Run this to create all tables.
"""

from sqlmodel import SQLModel, create_engine
from src.models.user import User
from src.models.task import Task
from src.core.config import get_settings

settings = get_settings()

def init_db():
    """Initialize database with all tables."""
    print("Creating database engine...")
    engine = create_engine(settings.database_url)

    print("Creating tables...")
    SQLModel.metadata.create_all(engine)

    print("✅ Database initialized successfully!")
    print(f"Database location: {settings.database_url}")

if __name__ == "__main__":
    init_db()
