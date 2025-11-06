"""Password reset service."""

from datetime import datetime, timedelta, timezone
from typing import Dict
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.user import user as user_crud
from app.utils.security import create_reset_token, verify_reset_token
from app.utils.email import email_service
from app.utils.email_templates import password_reset_email
from app.config import settings


class PasswordResetService:
    """Business logic for password reset flow."""

    def request_password_reset(self, db: Session, email: str) -> Dict[str, str]:
        """
        Request password reset for user email.

        Generates reset token, saves to DB, and sends email.
        Returns success message (doesn't reveal if email exists).
        """
        # Get user by email
        user = user_crud.get_by_email(db, email=email)

        # Always return success message to prevent email enumeration
        success_message = {
            "message": "If an account with that email exists, a password reset link has been sent."
        }

        if not user:
            # Don't reveal that email doesn't exist
            return success_message

        if not user.is_active:
            # Don't reveal that account is inactive
            return success_message

        # Generate reset token
        reset_token = create_reset_token(email=user.email)

        # Set token expiration (24 hours)
        expires = datetime.now(timezone.utc) + timedelta(hours=24)

        # Save token to database
        user_crud.set_reset_token(db, user=user, token=reset_token, expires=expires)

        # Create reset URL
        frontend_url = settings.CORS_ORIGINS[0] if settings.CORS_ORIGINS else "http://localhost:3000"
        reset_url = f"{frontend_url}/reset-password?token={reset_token}"

        # Send email
        email_data = {
            "user_name": user.full_name or user.username,
            "reset_url": reset_url,
            "expiry_hours": 24,
        }

        email_content = password_reset_email(email_data)

        try:
            email_service.send_email(
                to_emails=[user.email],
                subject=email_content["subject"],
                body_html=email_content["html"],
                body_text=email_content["text"],
            )
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to send password reset email: {e}")
            # Still return success to prevent enumeration

        return success_message

    def reset_password(
        self, db: Session, token: str, new_password: str
    ) -> Dict[str, str]:
        """
        Reset password using token.

        Validates token, checks password history, and updates password.
        """
        # Verify token
        email = verify_reset_token(token)

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token",
            )

        # Get user
        user = user_crud.get_by_email(db, email=email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token",
            )

        # Check if token matches and hasn't expired
        if user.reset_token != token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token",
            )

        if not user.reset_token_expires:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token",
            )

        if datetime.now(timezone.utc) > user.reset_token_expires:
            # Clear expired token
            user_crud.clear_reset_token(db, user=user)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has expired. Please request a new one.",
            )

        # Validate password strength
        if len(new_password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long",
            )

        # Check password history (prevent reuse of last 3 passwords)
        if user_crud.check_password_in_history(user, new_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot reuse any of your last 3 passwords",
            )

        # Update password (this also clears reset token and updates history)
        user_crud.update_password(db, user=user, new_password=new_password)

        return {"message": "Password has been reset successfully"}


password_reset_service = PasswordResetService()
