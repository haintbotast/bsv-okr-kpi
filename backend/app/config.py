"""Application configuration."""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache
from typing import List, Union


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "KPI Management System"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480  # 8 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "sqlite:////data/database/kpi.db"

    # CORS
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:5173"]
    CORS_ALLOW_CREDENTIALS: bool = True

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from comma-separated string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    # File Upload
    UPLOAD_DIR: str = "/data/uploads"
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    ALLOWED_EXTENSIONS: Union[List[str], str] = [
        "pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx",
        "jpg", "jpeg", "png", "gif"
    ]

    @field_validator('ALLOWED_EXTENSIONS', mode='before')
    @classmethod
    def parse_allowed_extensions(cls, v):
        """Parse ALLOWED_EXTENSIONS from comma-separated string or list."""
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(',')]
        return v

    # Backup
    BACKUP_DIR: str = "/data/backups"
    BACKUP_RETENTION_DAYS: int = 30
    AUTO_BACKUP_ENABLED: bool = True
    BACKUP_SCHEDULE: str = "0 2 * * *"  # Daily at 2 AM

    # Email (Optional)
    SMTP_ENABLED: bool = False
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@company.com"
    SMTP_TLS: bool = True

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "/data/logs/app.log"

    # Features
    ENABLE_REGISTRATION: bool = False
    ENABLE_DOCS: bool = True
    ENABLE_NOTIFICATIONS: bool = True

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
