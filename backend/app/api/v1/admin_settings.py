"""Admin API endpoints for system settings management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.api.deps import require_admin
from app.services.settings_service import settings_service

router = APIRouter()


class SMTPSettings(BaseModel):
    """SMTP configuration schema."""
    enabled: bool = False
    host: str = Field(..., min_length=1, max_length=255)
    port: int = Field(..., ge=1, le=65535)
    user: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1)
    from_email: EmailStr
    use_tls: bool = True


class SMTPSettingsResponse(BaseModel):
    """SMTP configuration response (without password)."""
    enabled: bool
    host: str
    port: int
    user: str
    from_email: str
    use_tls: bool


class TestEmailRequest(BaseModel):
    """Test email request schema."""
    to_email: EmailStr
    smtp_config: Optional[SMTPSettings] = None


class SettingsResponse(BaseModel):
    """Generic settings response."""
    success: bool
    message: str


@router.get("/smtp", response_model=SMTPSettingsResponse)
def get_smtp_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Get current SMTP settings (admin only).

    Password is not included in response for security.
    """
    smtp_config = settings_service.get_smtp_settings(db)

    return SMTPSettingsResponse(
        enabled=smtp_config["enabled"],
        host=smtp_config["host"],
        port=smtp_config["port"],
        user=smtp_config["user"],
        from_email=smtp_config["from_email"],
        use_tls=smtp_config["use_tls"]
    )


@router.put("/smtp", response_model=SettingsResponse)
def update_smtp_settings(
    smtp_settings: SMTPSettings,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update SMTP settings (admin only).

    Password will be encrypted before storage.
    """
    smtp_config = {
        "enabled": smtp_settings.enabled,
        "host": smtp_settings.host,
        "port": smtp_settings.port,
        "user": smtp_settings.user,
        "password": smtp_settings.password,
        "from_email": smtp_settings.from_email,
        "use_tls": smtp_settings.use_tls
    }

    success = settings_service.update_smtp_settings(db, smtp_config)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update SMTP settings"
        )

    return SettingsResponse(
        success=True,
        message="SMTP settings updated successfully"
    )


@router.post("/smtp/test-connection", response_model=SettingsResponse)
def test_smtp_connection(
    smtp_settings: SMTPSettings,
    current_user: User = Depends(require_admin)
):
    """
    Test SMTP connection without saving (admin only).

    Tests connection with provided credentials.
    """
    smtp_config = {
        "host": smtp_settings.host,
        "port": smtp_settings.port,
        "user": smtp_settings.user,
        "password": smtp_settings.password,
        "use_tls": smtp_settings.use_tls
    }

    result = settings_service.test_smtp_connection(smtp_config)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    return SettingsResponse(
        success=True,
        message=result["message"]
    )


@router.post("/smtp/send-test-email", response_model=SettingsResponse)
def send_test_email(
    request: TestEmailRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Send a test email (admin only).

    Can use either provided SMTP config or saved config.
    """
    # Use provided config or get from database
    if request.smtp_config:
        smtp_config = {
            "enabled": request.smtp_config.enabled,
            "host": request.smtp_config.host,
            "port": request.smtp_config.port,
            "user": request.smtp_config.user,
            "password": request.smtp_config.password,
            "from_email": request.smtp_config.from_email,
            "use_tls": request.smtp_config.use_tls
        }
    else:
        smtp_config = settings_service.get_smtp_settings(db)

    if not smtp_config.get("enabled", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="SMTP is not enabled"
        )

    result = settings_service.send_test_email(smtp_config, request.to_email)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    return SettingsResponse(
        success=True,
        message=result["message"]
    )
