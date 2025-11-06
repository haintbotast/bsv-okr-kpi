"""Encryption utilities for sensitive data."""

from cryptography.fernet import Fernet
import base64
import hashlib
from app.config import settings


class EncryptionService:
    """Service for encrypting/decrypting sensitive data."""

    def __init__(self):
        """Initialize encryption service with key derived from SECRET_KEY."""
        # Derive a Fernet-compatible key from SECRET_KEY
        key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
        self.cipher = Fernet(base64.urlsafe_b64encode(key))

    def encrypt(self, value: str) -> str:
        """
        Encrypt a string value.

        Args:
            value: Plain text string to encrypt

        Returns:
            Base64-encoded encrypted string
        """
        if not value:
            return ""

        encrypted = self.cipher.encrypt(value.encode())
        return encrypted.decode()

    def decrypt(self, encrypted_value: str) -> str:
        """
        Decrypt an encrypted string value.

        Args:
            encrypted_value: Base64-encoded encrypted string

        Returns:
            Decrypted plain text string
        """
        if not encrypted_value:
            return ""

        try:
            decrypted = self.cipher.decrypt(encrypted_value.encode())
            return decrypted.decode()
        except Exception:
            # If decryption fails, return empty string
            return ""


# Global encryption service instance
encryption_service = EncryptionService()
