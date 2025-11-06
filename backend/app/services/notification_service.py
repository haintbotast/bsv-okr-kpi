"""Enhanced notification service with email integration."""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import logging

from app.models.user import User
from app.models.notification import Notification
from app.crud import notification as notification_crud
from app.utils.email import email_service
from app.utils.email_templates import (
    kpi_submitted_email,
    kpi_approved_email,
    kpi_rejected_email,
    comment_mention_email,
    weekly_digest_email
)
from app.config import settings

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for managing notifications (in-app and email)."""

    def __init__(self):
        """Initialize notification service."""
        self.email_enabled = settings.SMTP_ENABLED

    def create_notification(
        self,
        db: Session,
        user_id: int,
        title: str,
        message: str,
        type: str = "info",
        link: Optional[str] = None,
        send_email: bool = True,
        email_template_data: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """
        Create an in-app notification and optionally send email.

        Args:
            db: Database session
            user_id: User ID to notify
            title: Notification title
            message: Notification message
            type: Notification type (info, success, warning, error)
            link: Optional link for the notification
            send_email: Whether to send email notification
            email_template_data: Data for email template

        Returns:
            Created notification
        """
        # Create in-app notification
        notification = notification_crud.create(
            db=db,
            user_id=user_id,
            title=title,
            message=message,
            type=type,
            link=link
        )

        # Send email if enabled and requested
        if send_email and email_template_data:
            user = db.query(User).filter(User.id == user_id).first()
            if user and user.email_notifications:
                self._send_email_notification(user=user, data=email_template_data)

        return notification

    def notify_kpi_submitted(
        self,
        db: Session,
        kpi_id: int,
        kpi_title: str,
        submitter: User,
        approvers: List[User],
        year: int,
        quarter: str
    ) -> None:
        """
        Notify approvers when a KPI is submitted.

        Args:
            db: Database session
            kpi_id: KPI ID
            kpi_title: KPI title
            submitter: User who submitted
            approvers: List of users who can approve
            year: KPI year
            quarter: KPI quarter
        """
        link = f"/kpis/{kpi_id}"
        base_url = settings.CORS_ORIGINS[0] if settings.CORS_ORIGINS else "http://localhost"
        full_link = f"{base_url}{link}"

        for approver in approvers:
            # Check notification preference
            if not approver.notify_kpi_submitted:
                continue

            # Create in-app notification
            title = "New KPI Submitted for Approval"
            message = f"{submitter.full_name or submitter.username} submitted a KPI: {kpi_title}"

            # Email template data
            email_data = {
                "kpi_title": kpi_title,
                "submitter_name": submitter.full_name or submitter.username,
                "year": year,
                "quarter": quarter,
                "link": full_link,
                "template": "kpi_submitted"
            }

            self.create_notification(
                db=db,
                user_id=approver.id,
                title=title,
                message=message,
                type="info",
                link=link,
                send_email=True,
                email_template_data=email_data
            )

            logger.info(f"Notified user {approver.id} about KPI {kpi_id} submission")

    def notify_kpi_approved(
        self,
        db: Session,
        kpi_id: int,
        kpi_title: str,
        owner: User,
        approver: User,
        year: int,
        quarter: str
    ) -> None:
        """
        Notify KPI owner when their KPI is approved.

        Args:
            db: Database session
            kpi_id: KPI ID
            kpi_title: KPI title
            owner: KPI owner
            approver: User who approved
            year: KPI year
            quarter: KPI quarter
        """
        # Check notification preference
        if not owner.notify_kpi_approved:
            return

        link = f"/kpis/{kpi_id}"
        base_url = settings.CORS_ORIGINS[0] if settings.CORS_ORIGINS else "http://localhost"
        full_link = f"{base_url}{link}"

        title = "✅ Your KPI Has Been Approved"
        message = f"{approver.full_name or approver.username} approved your KPI: {kpi_title}"

        email_data = {
            "kpi_title": kpi_title,
            "approver_name": approver.full_name or approver.username,
            "year": year,
            "quarter": quarter,
            "link": full_link,
            "template": "kpi_approved"
        }

        self.create_notification(
            db=db,
            user_id=owner.id,
            title=title,
            message=message,
            type="success",
            link=link,
            send_email=True,
            email_template_data=email_data
        )

        logger.info(f"Notified user {owner.id} about KPI {kpi_id} approval")

    def notify_kpi_rejected(
        self,
        db: Session,
        kpi_id: int,
        kpi_title: str,
        owner: User,
        approver: User,
        year: int,
        quarter: str,
        reason: Optional[str] = None
    ) -> None:
        """
        Notify KPI owner when their KPI is rejected.

        Args:
            db: Database session
            kpi_id: KPI ID
            kpi_title: KPI title
            owner: KPI owner
            approver: User who rejected
            year: KPI year
            quarter: KPI quarter
            reason: Rejection reason
        """
        # Check notification preference
        if not owner.notify_kpi_rejected:
            return

        link = f"/kpis/{kpi_id}"
        base_url = settings.CORS_ORIGINS[0] if settings.CORS_ORIGINS else "http://localhost"
        full_link = f"{base_url}{link}"

        title = "❌ Your KPI Requires Changes"
        message = f"{approver.full_name or approver.username} rejected your KPI: {kpi_title}"
        if reason:
            message += f" - Reason: {reason}"

        email_data = {
            "kpi_title": kpi_title,
            "approver_name": approver.full_name or approver.username,
            "year": year,
            "quarter": quarter,
            "reason": reason,
            "link": full_link,
            "template": "kpi_rejected"
        }

        self.create_notification(
            db=db,
            user_id=owner.id,
            title=title,
            message=message,
            type="warning",
            link=link,
            send_email=True,
            email_template_data=email_data
        )

        logger.info(f"Notified user {owner.id} about KPI {kpi_id} rejection")

    def notify_comment_mention(
        self,
        db: Session,
        kpi_id: int,
        kpi_title: str,
        mentioned_user: User,
        commenter: User,
        comment_text: str
    ) -> None:
        """
        Notify user when they are mentioned in a comment.

        Args:
            db: Database session
            kpi_id: KPI ID
            kpi_title: KPI title
            mentioned_user: User who was mentioned
            commenter: User who made the comment
            comment_text: Comment text
        """
        # Check notification preference
        if not mentioned_user.notify_comment_mention:
            return

        link = f"/kpis/{kpi_id}"
        base_url = settings.CORS_ORIGINS[0] if settings.CORS_ORIGINS else "http://localhost"
        full_link = f"{base_url}{link}"

        title = "💬 You Were Mentioned in a Comment"
        message = f"{commenter.full_name or commenter.username} mentioned you in a comment on: {kpi_title}"

        email_data = {
            "kpi_title": kpi_title,
            "commenter_name": commenter.full_name or commenter.username,
            "comment_text": comment_text[:200],  # Limit to 200 chars
            "link": full_link,
            "template": "comment_mention"
        }

        self.create_notification(
            db=db,
            user_id=mentioned_user.id,
            title=title,
            message=message,
            type="info",
            link=link,
            send_email=True,
            email_template_data=email_data
        )

        logger.info(f"Notified user {mentioned_user.id} about mention in KPI {kpi_id}")

    def _send_email_notification(self, user: User, data: Dict[str, Any]) -> bool:
        """
        Send email notification using template.

        Args:
            user: User to send email to
            data: Template data including 'template' key

        Returns:
            True if sent successfully
        """
        if not self.email_enabled:
            logger.debug("Email notifications disabled")
            return False

        if not user.email:
            logger.warning(f"User {user.id} has no email address")
            return False

        # Get template based on type
        template_name = data.get("template")
        email_content = None

        if template_name == "kpi_submitted":
            email_content = kpi_submitted_email(data)
        elif template_name == "kpi_approved":
            email_content = kpi_approved_email(data)
        elif template_name == "kpi_rejected":
            email_content = kpi_rejected_email(data)
        elif template_name == "comment_mention":
            email_content = comment_mention_email(data)
        elif template_name == "weekly_digest":
            email_content = weekly_digest_email(data)
        else:
            logger.error(f"Unknown email template: {template_name}")
            return False

        # Send email
        success = email_service.send_email(
            to_emails=[user.email],
            subject=email_content["subject"],
            body_html=email_content["html_body"],
            body_text=email_content.get("text_body")
        )

        return success


# Global notification service instance
notification_service = NotificationService()
