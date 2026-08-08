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
    app_version: str = "0.1.0"
    environment: Literal["development", "test", "production"] = "development"
    ai_provider: Literal["stub"] = "stub"
    request_id_header: str = "X-Request-ID"
    expose_error_details: bool = False

    database_url: str = Field(
        default="sqlite:///./local.db",
        description="Reserved for the persistence milestone.",
    )
    openai_api_key: str | None = Field(
        default=None,
        description="Reserved for a later production provider milestone.",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
