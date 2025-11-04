"""CRUD operations for Notifications."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.notification import Notification


class NotificationCRUD:
    """CRUD operations for Notifications."""

    def create(
        self,
        db: Session,
        *,
        user_id: int,
        title: str,
        message: str,
        notification_type: str = "info",
        link: Optional[str] = None
    ) -> Notification:
        """Create new notification.

        Args:
            db: Database session
            user_id: User ID to send notification to
            title: Notification title
            message: Notification message
            notification_type: Type (info, warning, success, error)
            link: Optional link URL

        Returns:
            Created Notification object
        """
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            link=link,
            is_read=False
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    def get(self, db: Session, *, notification_id: int) -> Optional[Notification]:
        """Get notification by ID.

        Args:
            db: Database session
            notification_id: Notification ID

        Returns:
            Notification object or None
        """
        return db.query(Notification).filter(Notification.id == notification_id).first()

    def get_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 50,
        unread_only: bool = False
    ) -> List[Notification]:
        """Get notifications for a user.

        Args:
            db: Database session
            user_id: User ID
            skip: Number of notifications to skip
            limit: Maximum number of notifications to return
            unread_only: Only return unread notifications

        Returns:
            List of Notification objects
        """
        query = db.query(Notification).filter(Notification.user_id == user_id)

        if unread_only:
            query = query.filter(Notification.is_read == False)

        return (
            query
            .order_by(Notification.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def mark_as_read(
        self,
        db: Session,
        *,
        notification_id: int
    ) -> Optional[Notification]:
        """Mark notification as read.

        Args:
            db: Database session
            notification_id: Notification ID

        Returns:
            Updated Notification object or None
        """
        notification = self.get(db, notification_id=notification_id)
        if not notification:
            return None

        notification.is_read = True
        db.commit()
        db.refresh(notification)
        return notification

    def mark_all_as_read(self, db: Session, *, user_id: int) -> int:
        """Mark all notifications as read for a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            Number of notifications marked as read
        """
        count = (
            db.query(Notification)
            .filter(Notification.user_id == user_id, Notification.is_read == False)
            .update({"is_read": True})
        )
        db.commit()
        return count

    def delete(self, db: Session, *, notification_id: int) -> bool:
        """Delete notification by ID.

        Args:
            db: Database session
            notification_id: Notification ID

        Returns:
            True if deleted, False if not found
        """
        notification = self.get(db, notification_id=notification_id)
        if not notification:
            return False

        db.delete(notification)
        db.commit()
        return True

    def count_unread(self, db: Session, *, user_id: int) -> int:
        """Count unread notifications for a user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            Number of unread notifications
        """
        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id, Notification.is_read == False)
            .count()
        )

    def delete_old_notifications(
        self,
        db: Session,
        *,
        days: int = 30
    ) -> int:
        """Delete old read notifications.

        Args:
            db: Database session
            days: Delete notifications older than this many days

        Returns:
            Number of notifications deleted
        """
        from datetime import datetime, timezone, timedelta

        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

        count = (
            db.query(Notification)
            .filter(
                Notification.is_read == True,
                Notification.created_at < cutoff_date
            )
            .delete()
        )
        db.commit()
        return count


# Create singleton instance
notification_crud = NotificationCRUD()
