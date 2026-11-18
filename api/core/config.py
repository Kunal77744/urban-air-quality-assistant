"""Application configuration loaded from environment variables."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Immutable application settings validated at startup."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Urban Air Quality Assistant"
    env: str = Field(default="production", description="Runtime environment")
    debug: bool = Field(default=False, description="Enable debug mode")

    gemini_api_key: str | None = Field(
        default=None,
        description="Optional Gemini API key for natural text enhancement",
    )
    gemini_model: str = Field(
        default="gemini-2.5-flash",
        description="Gemini model identifier",
    )

    rate_limit_per_minute: int = Field(
        default=60,
        ge=1,
        le=300,
        description="Maximum requests per IP per minute",
    )
    cors_allowed_origins: list[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed CORS origin list",
    )


def get_settings() -> Settings:
    """Return an initialized Settings instance."""
    return Settings()
