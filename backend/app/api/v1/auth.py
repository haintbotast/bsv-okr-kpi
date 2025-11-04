"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest
from app.schemas.user import UserResponse
from app.services.auth import auth_service
from app.models.user import User

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Login with email and password.

    Returns access token, refresh token, and user information.
    """
    return auth_service.login(db, credentials)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Refresh access token using refresh token.

    Returns new access token and refresh token.
    """
    return auth_service.refresh_token(db, refresh_data.refresh_token)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get current user information.

    Requires valid access token.
    """
    return current_user


@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_active_user),
):
    """
    Logout current user.

    Note: With JWT, logout is handled client-side by removing tokens.
    This endpoint is optional and can be used for logging/auditing.
    """
    return {"message": "Successfully logged out"}
