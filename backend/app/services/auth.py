"""Authentication service."""

from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.crud.user import user as user_crud
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    verify_token,
)
from app.config import settings


class AuthService:
    """Authentication business logic."""

    def login(self, db: Session, credentials: LoginRequest) -> TokenResponse:
        """Authenticate user and return tokens."""
        # Authenticate user
        user = user_crud.authenticate(
            db, email=credentials.email, password=credentials.password
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user_crud.is_active(user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        # Create tokens
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role}
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "email": user.email}
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user),
        )

    def refresh_token(self, db: Session, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token."""
        # Verify refresh token
        payload = verify_token(refresh_token, token_type="refresh")

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Get user
        user_id = int(payload.get("sub"))
        user = user_crud.get(db, user_id=user_id)

        if not user or not user_crud.is_active(user):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        # Create new tokens
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role}
        )
        new_refresh_token = create_refresh_token(
            data={"sub": str(user.id), "email": user.email}
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user),
        )


auth_service = AuthService()
