"""
Configuration management for Cloud Cost Optimizer
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""

    # Basic settings
    debug: bool = True
    log_level: str = "INFO"
    secret_key: str = "your-secret-key-change-in-production"

    # Database
    database_url: str = "sqlite:///./cost_optimizer.db"

    # AWS Settings
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_default_region: str = "ap-south-1"

    # Azure Settings
    azure_client_id: Optional[str] = None
    azure_client_secret: Optional[str] = None
    azure_tenant_id: Optional[str] = None

    # GCP Settings
    google_application_credentials: Optional[str] = None
    gcp_project_id: Optional[str] = None

    # Indian Market Settings
    currency: str = "INR"
    timezone: str = "Asia/Kolkata"
    language: str = "en-IN"

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False

def get_settings() -> Settings:
    """Get application settings"""
    return Settings()
