from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="CHIMERA_",
        extra="ignore",
    )

    app_name: str = "Project Chimera API"
    app_version: str = "0.2.0"
    environment: Literal["development", "test", "production"] = "development"
    ai_provider: Literal["stub", "openai"] = "stub"
    request_id_header: str = "X-Request-ID"
    expose_error_details: bool = False
    demo_mode: bool = Field(
        default=False,
        description="Prefer deterministic stub behavior for reliable demos.",
    )
    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Comma-separated allowed CORS origins.",
    )
    max_message_length: int = Field(default=8000, ge=256, le=50000)

    database_url: str = Field(
        default="sqlite:///./local.db",
        description="SQLAlchemy database URL.",
    )
    openai_api_key: str | None = Field(
        default=None,
        description="OpenAI API key. Never commit real secrets.",
    )
    openai_model: str = Field(default="gpt-4o-mini")
    openai_timeout_seconds: float = Field(default=30.0, gt=0)
    openai_max_retries: int = Field(default=2, ge=0, le=5)


@lru_cache
def get_settings() -> Settings:
    return Settings()
