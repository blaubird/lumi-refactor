import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings"""
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    
    # WhatsApp API
    WH_TOKEN: str = Field(..., env="WH_TOKEN")
    
    # AI Service
    OPENAI_API_KEY: str = Field(None, env="OPENAI_API_KEY")
    
    # Logging
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()
