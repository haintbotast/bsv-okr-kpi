"""Notification API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.schemas.notification import (
    NotificationResponse,
    NotificationUpdate,
    UnreadCount
)
from app.crud.notification import notification_crud

router = APIRouter()


@router.get("/notifications", response_model=List[NotificationResponse])
def list_notifications(
    skip: int = 0,
    limit: int = 50,
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List notifications for current user.

    **Args:**
    - skip: Number of notifications to skip (pagination)
    - limit: Maximum number of notifications to return
    - unread_only: Only return unread notifications

    **Returns:**
    - List of notifications
    """
    notifications = notification_crud.get_by_user(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        unread_only=unread_only
    )
    return notifications


@router.get("/notifications/unread-count", response_model=UnreadCount)
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get count of unread notifications for current user.

    **Returns:**
    - Count of unread notifications
    """
    count = notification_crud.count_unread(db, user_id=current_user.id)
    return {"count": count}


@router.put("/notifications/{notification_id}", response_model=NotificationResponse)
def update_notification(
    notification_id: int,
    notification_in: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a notification (mark as read/unread).

    **Args:**
    - notification_id: Notification ID
    - notification_in: Update data

    **Returns:**
    - Updated notification
    """
    # Get notification
    notification = notification_crud.get(db, notification_id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    # Check ownership
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own notifications"
        )

    # Mark as read
    if notification_in.is_read is not None:
        updated_notification = notification_crud.mark_as_read(
            db,
            notification_id=notification_id
        )
        return updated_notification

    return notification


@router.post("/notifications/mark-all-read")
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Mark all notifications as read for current user.

    **Returns:**
    - Count of notifications marked as read
    """
    count = notification_crud.mark_all_as_read(db, user_id=current_user.id)
    return {"count": count, "message": f"Marked {count} notifications as read"}


@router.delete("/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a notification.

    **Args:**
    - notification_id: Notification ID to delete
    """
    # Get notification
    notification = notification_crud.get(db, notification_id=notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    # Check ownership
    if notification.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own notifications"
        )

    notification_crud.delete(db, notification_id=notification_id)
    return None
