import os
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BeforeValidator, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    PROJECT_NAME: str = "AI Job Automation Platform"
    API_V1_STR: str = "/api/v1"
    
    # JWT Configs
    SECRET_KEY: str = "supersecretkeychangeinproduction1234567890"  # Fallback for dev only
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # DB Configs
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_job"
    REDIS_URL: str = "redis://localhost:6379/0"

    # AI API Keys
    OPENAI_API_KEY: Optional[str] = None
    CLAUDE_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None

    @property
    def async_database_url(self) -> str:
        """Ensure database URL uses postgresql+asyncpg driver."""
        url = self.DATABASE_URL
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url


settings = Settings()
