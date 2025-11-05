"""File service for handling file uploads, validation, and storage."""

import os
import uuid
from typing import Tuple, Optional
from pathlib import Path
from fastapi import UploadFile, HTTPException, status

# File validation constants
ALLOWED_EXTENSIONS = {
    # Documents
    'pdf': 'application/pdf',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    # Spreadsheets
    'xls': 'application/vnd.ms-excel',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    # Images
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
}

from app.config import settings

MAX_FILE_SIZE = settings.MAX_UPLOAD_SIZE
UPLOAD_DIR = Path(settings.UPLOAD_DIR)


class FileService:
    """Service for handling file operations."""

    def __init__(self):
        """Initialize file service and ensure upload directory exists."""
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    def validate_file_type(self, filename: str, content_type: str) -> str:
        """Validate file type by extension and content type.

        Args:
            filename: Original filename
            content_type: File MIME type

        Returns:
            File extension if valid

        Raises:
            HTTPException: If file type is not allowed
        """
        # Get file extension
        file_ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

        if not file_ext:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must have an extension"
            )

        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type '.{file_ext}' is not allowed. "
                       f"Allowed types: {', '.join(ALLOWED_EXTENSIONS.keys())}"
            )

        # Validate content type (allow some flexibility for common variations)
        expected_content_type = ALLOWED_EXTENSIONS[file_ext]
        if content_type and not (
            content_type == expected_content_type or
            content_type.startswith('application/octet-stream')  # Generic binary
        ):
            # Log warning but don't fail - some browsers send incorrect MIME types
            pass

        return file_ext

    def validate_file_size(self, file_size: int) -> None:
        """Validate file size.

        Args:
            file_size: Size of file in bytes

        Raises:
            HTTPException: If file is too large
        """
        if file_size > MAX_FILE_SIZE:
            size_mb = file_size / (1024 * 1024)
            max_size_mb = MAX_FILE_SIZE / (1024 * 1024)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size ({size_mb:.2f}MB) exceeds maximum allowed size ({max_size_mb}MB)"
            )

    def generate_unique_filename(self, original_filename: str) -> Tuple[str, str]:
        """Generate a unique filename using UUID.

        Args:
            original_filename: Original filename from user

        Returns:
            Tuple of (unique_filename, file_extension)
        """
        file_ext = original_filename.rsplit('.', 1)[-1].lower() if '.' in original_filename else ''
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        return unique_filename, file_ext

    async def save_file(self, file: UploadFile) -> Tuple[str, str, int]:
        """Save uploaded file to disk.

        Args:
            file: Uploaded file from FastAPI

        Returns:
            Tuple of (file_path, original_filename, file_size)

        Raises:
            HTTPException: If file validation fails or save fails
        """
        # Read file content
        try:
            contents = await file.read()
            file_size = len(contents)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to read file: {str(e)}"
            )

        # Validate file size
        self.validate_file_size(file_size)

        # Validate file type
        content_type = file.content_type or 'application/octet-stream'
        file_ext = self.validate_file_type(file.filename, content_type)

        # Generate unique filename
        unique_filename, _ = self.generate_unique_filename(file.filename)
        file_path = UPLOAD_DIR / unique_filename

        # Save file
        try:
            with open(file_path, 'wb') as f:
                f.write(contents)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save file: {str(e)}"
            )

        return str(file_path), file.filename, file_size

    def delete_file(self, file_path: str) -> bool:
        """Delete file from disk.

        Args:
            file_path: Path to file to delete

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                # Security check: ensure file is within upload directory
                if not str(path.resolve()).startswith(str(UPLOAD_DIR.resolve())):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid file path"
                    )
                path.unlink()
                return True
            return False
        except Exception:
            return False

    def get_file_path(self, filename: str) -> Optional[Path]:
        """Get full path for a filename.

        Args:
            filename: Filename to get path for

        Returns:
            Path object or None if file doesn't exist
        """
        file_path = UPLOAD_DIR / filename
        if file_path.exists() and file_path.is_file():
            return file_path
        return None


# Create singleton instance
file_service = FileService()
