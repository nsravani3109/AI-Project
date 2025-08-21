"""
Configuration module for the Inbound Sales AI Agent
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    api_key: str = "default-api-key"
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: str = "sqlite:///./loads.db"
    redis_url: str = "redis://localhost:6379"
    
    # External APIs
    happyrobot_api_key: Optional[str] = None
    happyrobot_base_url: str = "https://api.happyrobot.ai"
    fmcsa_api_base_url: str = "https://mobile.fmcsa.dot.gov/qc/services/carriers"
    # fmcsa_api_key: str = "cdc33e44d693a3a58451898d4ec9df862c65b954"
    fmcsa_api_key: str = ""
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
