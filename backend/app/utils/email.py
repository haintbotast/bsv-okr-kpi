"""Email utility functions for sending notifications."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from datetime import datetime, timezone
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending notifications."""

    def __init__(self):
        """Initialize email service."""
        self.enabled = settings.SMTP_ENABLED
        self.host = settings.SMTP_HOST
        self.port = settings.SMTP_PORT
        self.user = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM
        self.use_tls = settings.SMTP_TLS

    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        body_html: str,
        body_text: Optional[str] = None
    ) -> bool:
        """
        Send an email.

        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            body_html: HTML email body
            body_text: Plain text email body (fallback)

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            logger.warning("Email service is disabled. Email not sent.")
            return False

        if not to_emails:
            logger.warning("No recipients specified. Email not sent.")
            return False

        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.from_email
            message["To"] = ", ".join(to_emails)
            message["Date"] = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

            # Add plain text version if provided
            if body_text:
                part1 = MIMEText(body_text, "plain")
                message.attach(part1)

            # Add HTML version
            part2 = MIMEText(body_html, "html")
            message.attach(part2)

            # Connect and send
            with smtplib.SMTP(self.host, self.port) as server:
                if self.use_tls:
                    server.starttls()
                if self.user and self.password:
                    server.login(self.user, self.password)
                server.send_message(message)

            logger.info(f"Email sent successfully to {', '.join(to_emails)}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False


# Global email service instance
email_service = EmailService()
