"""API endpoints for user preferences."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.api.deps import get_current_active_user
from app.schemas.user import NotificationPreferences, UserResponse

router = APIRouter()


@router.get("/notification-preferences", response_model=NotificationPreferences)
def get_notification_preferences(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's notification preferences.
    """
    return NotificationPreferences(
        email_notifications=current_user.email_notifications,
        notify_kpi_submitted=current_user.notify_kpi_submitted,
        notify_kpi_approved=current_user.notify_kpi_approved,
        notify_kpi_rejected=current_user.notify_kpi_rejected,
        notify_comment_mention=current_user.notify_comment_mention,
        weekly_digest=current_user.weekly_digest
    )


@router.put("/notification-preferences", response_model=UserResponse)
def update_notification_preferences(
    preferences: NotificationPreferences,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update current user's notification preferences.
    """
    # Update preferences
    current_user.email_notifications = preferences.email_notifications
    current_user.notify_kpi_submitted = preferences.notify_kpi_submitted
    current_user.notify_kpi_approved = preferences.notify_kpi_approved
    current_user.notify_kpi_rejected = preferences.notify_kpi_rejected
    current_user.notify_comment_mention = preferences.notify_comment_mention
    current_user.weekly_digest = preferences.weekly_digest

    db.commit()
    db.refresh(current_user)

    return current_user


@router.post("/notification-preferences/reset", response_model=UserResponse)
def reset_notification_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Reset notification preferences to default (all enabled).
    """
    current_user.email_notifications = True
    current_user.notify_kpi_submitted = True
    current_user.notify_kpi_approved = True
    current_user.notify_kpi_rejected = True
    current_user.notify_comment_mention = True
    current_user.weekly_digest = True

    db.commit()
    db.refresh(current_user)

    return current_user
