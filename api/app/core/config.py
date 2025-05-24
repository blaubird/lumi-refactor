"""Config module."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = "Lumi API"
    PROJECT_DESCRIPTION: str = "AI-powered knowledge base API"
    PROJECT_VERSION: str = "0.1.0"

    DATABASE_URL: str = "sqlite:///./lumi.db"

    CORS_ORIGINS: list = ["*"]

    OPENAI_MODEL: str = "gpt-3.5-turbo"

    class Config:
        """Pydantic config."""

        env_file = ".env"


settings = Settings()
