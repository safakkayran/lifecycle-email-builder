"""Configuration settings for lifecycle-email-builder."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LiteLLM
    LLM_MODEL: str = Field(default="nim-laguna", description="Worker model alias")
    LLM_JUDGE_MODEL: str = Field(default="nim-step", description="Judge model alias")
    LITELLM_BASE_URL: str = Field(
        default="http://127.0.0.1:4000", description="LiteLLM proxy base URL"
    )
    LITELLM_API_KEY: str | None = Field(default=None, description="LiteLLM master key")

    # GitHub
    GITHUB_TOKEN: str | None = Field(default=None, description="GitHub PAT for API")

    # Paths
    VENDOR_DIR: Path = Field(default=Path("vendor/marketingskills"))
    OUTPUT_DIR: Path = Field(default=Path("out"))
    CACHE_DIR: Path = Field(default=Path(".cache/lifecycle_builder"))

    # Skill loading
    SKILL_CONTEXT_MAX_CHARS: int = Field(default=12000)

    # Node for MJML
    NODE_BIN: str = Field(default="npx", description="Node package runner (npx)")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()