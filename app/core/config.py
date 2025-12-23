"""Configuration management using environment variables"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    api_title: str = "TaskFlow API"
    api_version: str = "1.0.0"
    api_description: str = "Scalable Task Queue & API Service"
    
    # Database Configuration
    database_url: str = "sqlite:///./taskflow.db"
    
    # Security
    api_key: Optional[str] = None
    secret_key: str = "dev-secret-key-change-in-production"
    
    # Worker Configuration
    worker_enabled: bool = True
    worker_concurrency: int = 4
    worker_poll_interval: int = 5  # seconds
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # CORS
    cors_origins: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

