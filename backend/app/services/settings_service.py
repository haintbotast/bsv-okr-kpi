"""Service for managing system settings."""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
import json
import smtplib
from email.mime.text import MIMEText
import logging

from app.models.system import SystemSettings
from app.utils.encryption import encryption_service
from app.config import settings as app_settings

logger = logging.getLogger(__name__)


class SettingsService:
    """Service for managing system settings with DB storage."""

    # Settings keys
    KEY_SMTP_ENABLED = "smtp_enabled"
    KEY_SMTP_HOST = "smtp_host"
    KEY_SMTP_PORT = "smtp_port"
    KEY_SMTP_USER = "smtp_user"
    KEY_SMTP_PASSWORD = "smtp_password"  # Encrypted
    KEY_SMTP_FROM = "smtp_from"
    KEY_SMTP_TLS = "smtp_tls"

    def get_setting(self, db: Session, key: str, default: Any = None) -> Any:
        """
        Get a setting value from database or environment.

        Priority: Database > Environment > Default

        Args:
            db: Database session
            key: Setting key
            default: Default value if not found

        Returns:
            Setting value
        """
        # Try database first
        setting = db.query(SystemSettings).filter(
            SystemSettings.key == key
        ).first()

        if setting:
            # Handle encrypted values
            if key == self.KEY_SMTP_PASSWORD and setting.value:
                return encryption_service.decrypt(setting.value)

            # Parse JSON values
            try:
                return json.loads(setting.value)
            except (json.JSONDecodeError, TypeError):
                return setting.value

        # Fall back to environment variables
        env_value = self._get_from_env(key)
        if env_value is not None:
            return env_value

        # Return default
        return default

    def set_setting(
        self,
        db: Session,
        key: str,
        value: Any,
        encrypt: bool = False
    ) -> SystemSettings:
        """
        Set a setting value in database.

        Args:
            db: Database session
            key: Setting key
            value: Setting value
            encrypt: Whether to encrypt the value

        Returns:
            SystemSettings object
        """
        # Get or create setting
        setting = db.query(SystemSettings).filter(
            SystemSettings.key == key
        ).first()

        if not setting:
            setting = SystemSettings(key=key)
            db.add(setting)

        # Convert value to string
        if isinstance(value, (dict, list)):
            value_str = json.dumps(value)
        elif isinstance(value, bool):
            value_str = json.dumps(value)
        else:
            value_str = str(value)

        # Encrypt if needed
        if encrypt and value_str:
            value_str = encryption_service.encrypt(value_str)

        setting.value = value_str
        db.commit()
        db.refresh(setting)

        return setting

    def get_smtp_settings(self, db: Session) -> Dict[str, Any]:
        """
        Get SMTP settings from database or environment.

        Returns:
            Dict with SMTP configuration
        """
        return {
            "enabled": self.get_setting(db, self.KEY_SMTP_ENABLED, app_settings.SMTP_ENABLED),
            "host": self.get_setting(db, self.KEY_SMTP_HOST, app_settings.SMTP_HOST),
            "port": self.get_setting(db, self.KEY_SMTP_PORT, app_settings.SMTP_PORT),
            "user": self.get_setting(db, self.KEY_SMTP_USER, app_settings.SMTP_USER),
            "password": self.get_setting(db, self.KEY_SMTP_PASSWORD, app_settings.SMTP_PASSWORD),
            "from_email": self.get_setting(db, self.KEY_SMTP_FROM, app_settings.SMTP_FROM),
            "use_tls": self.get_setting(db, self.KEY_SMTP_TLS, app_settings.SMTP_TLS),
        }

    def update_smtp_settings(self, db: Session, smtp_config: Dict[str, Any]) -> bool:
        """
        Update SMTP settings in database.

        Args:
            db: Database session
            smtp_config: SMTP configuration dict

        Returns:
            True if updated successfully
        """
        try:
            # Update each setting
            if "enabled" in smtp_config:
                self.set_setting(db, self.KEY_SMTP_ENABLED, smtp_config["enabled"])

            if "host" in smtp_config:
                self.set_setting(db, self.KEY_SMTP_HOST, smtp_config["host"])

            if "port" in smtp_config:
                self.set_setting(db, self.KEY_SMTP_PORT, smtp_config["port"])

            if "user" in smtp_config:
                self.set_setting(db, self.KEY_SMTP_USER, smtp_config["user"])

            if "password" in smtp_config:
                # Encrypt password
                self.set_setting(db, self.KEY_SMTP_PASSWORD, smtp_config["password"], encrypt=True)

            if "from_email" in smtp_config:
                self.set_setting(db, self.KEY_SMTP_FROM, smtp_config["from_email"])

            if "use_tls" in smtp_config:
                self.set_setting(db, self.KEY_SMTP_TLS, smtp_config["use_tls"])

            return True

        except Exception as e:
            logger.error(f"Failed to update SMTP settings: {str(e)}")
            return False

    def test_smtp_connection(self, smtp_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test SMTP connection with given configuration.

        Args:
            smtp_config: SMTP configuration dict

        Returns:
            Dict with success status and message
        """
        try:
            host = smtp_config.get("host")
            port = smtp_config.get("port", 587)
            user = smtp_config.get("user")
            password = smtp_config.get("password")
            use_tls = smtp_config.get("use_tls", True)

            if not host:
                return {"success": False, "message": "SMTP host is required"}

            # Try to connect
            with smtplib.SMTP(host, port, timeout=10) as server:
                if use_tls:
                    server.starttls()

                if user and password:
                    server.login(user, password)

                return {
                    "success": True,
                    "message": f"Successfully connected to {host}:{port}"
                }

        except smtplib.SMTPAuthenticationError:
            return {
                "success": False,
                "message": "Authentication failed. Check username and password."
            }
        except smtplib.SMTPConnectError:
            return {
                "success": False,
                "message": f"Could not connect to {host}:{port}. Check host and port."
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}"
            }

    def send_test_email(
        self,
        smtp_config: Dict[str, Any],
        to_email: str
    ) -> Dict[str, Any]:
        """
        Send a test email using given SMTP configuration.

        Args:
            smtp_config: SMTP configuration dict
            to_email: Recipient email address

        Returns:
            Dict with success status and message
        """
        try:
            host = smtp_config.get("host")
            port = smtp_config.get("port", 587)
            user = smtp_config.get("user")
            password = smtp_config.get("password")
            from_email = smtp_config.get("from_email", user)
            use_tls = smtp_config.get("use_tls", True)

            # Create test message
            message = MIMEText(
                "This is a test email from your KPI Management System.\n\n"
                "If you received this email, your SMTP configuration is working correctly!\n\n"
                "You can now enable email notifications for your users.",
                "plain"
            )
            message["Subject"] = "[TEST] KPI Management System - Email Configuration Test"
            message["From"] = from_email
            message["To"] = to_email

            # Send email
            with smtplib.SMTP(host, port, timeout=10) as server:
                if use_tls:
                    server.starttls()

                if user and password:
                    server.login(user, password)

                server.send_message(message)

            return {
                "success": True,
                "message": f"Test email sent successfully to {to_email}"
            }

        except Exception as e:
            logger.error(f"Failed to send test email: {str(e)}")
            return {
                "success": False,
                "message": f"Failed to send test email: {str(e)}"
            }

    def _get_from_env(self, key: str) -> Optional[Any]:
        """Get setting value from environment variables."""
        env_map = {
            self.KEY_SMTP_ENABLED: app_settings.SMTP_ENABLED,
            self.KEY_SMTP_HOST: app_settings.SMTP_HOST,
            self.KEY_SMTP_PORT: app_settings.SMTP_PORT,
            self.KEY_SMTP_USER: app_settings.SMTP_USER,
            self.KEY_SMTP_PASSWORD: app_settings.SMTP_PASSWORD,
            self.KEY_SMTP_FROM: app_settings.SMTP_FROM,
            self.KEY_SMTP_TLS: app_settings.SMTP_TLS,
        }
        return env_map.get(key)


# Global settings service instance
settings_service = SettingsService()
