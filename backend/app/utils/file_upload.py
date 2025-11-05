"""File upload utilities for handling avatar and file uploads."""

import os
import uuid
from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException, status
from pathlib import Path


# Allowed file extensions for avatars
ALLOWED_AVATAR_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# Maximum file size (5MB for avatars)
MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5MB in bytes

# Upload directory
UPLOAD_DIR = Path("/data/uploads")
AVATAR_DIR = UPLOAD_DIR / "avatars"


def ensure_upload_dirs():
    """Create upload directories if they don't exist."""
    AVATAR_DIR.mkdir(parents=True, exist_ok=True)


def validate_image_file(file: UploadFile, max_size: int = MAX_AVATAR_SIZE) -> None:
    """
    Validate uploaded image file.

    Args:
        file: The uploaded file
        max_size: Maximum allowed file size in bytes

    Raises:
        HTTPException: If validation fails
    """
    # Check if file exists
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )

    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_AVATAR_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_AVATAR_EXTENSIONS)}"
        )

    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning

    if file_size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size: {max_size_mb}MB"
        )


async def save_upload_file(
    file: UploadFile,
    directory: Path,
    filename: Optional[str] = None
) -> Tuple[str, str]:
    """
    Save uploaded file to disk.

    Args:
        file: The uploaded file
        directory: Directory to save file in
        filename: Optional filename (if not provided, generates UUID)

    Returns:
        Tuple of (file_path, filename)
    """
    # Generate unique filename if not provided
    if filename is None:
        file_ext = Path(file.filename).suffix.lower()
        filename = f"{uuid.uuid4()}{file_ext}"

    # Ensure directory exists
    directory.mkdir(parents=True, exist_ok=True)

    # Full path
    file_path = directory / filename

    # Save file
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    return str(file_path), filename


async def save_avatar(file: UploadFile) -> str:
    """
    Save avatar image and return the URL path.

    Args:
        file: The uploaded avatar file

    Returns:
        URL path to access the avatar (e.g., "/uploads/avatars/uuid.jpg")

    Raises:
        HTTPException: If validation fails
    """
    # Validate file
    validate_image_file(file)

    # Save file
    file_path, filename = await save_upload_file(file, AVATAR_DIR)

    # Return URL path
    return f"/uploads/avatars/{filename}"


def delete_file(file_path: str) -> bool:
    """
    Delete a file from disk.

    Args:
        file_path: Path to the file (can be URL path or full path)

    Returns:
        True if deleted, False if file doesn't exist
    """
    # Convert URL path to full path if needed
    if file_path.startswith("/uploads/"):
        file_path = str(UPLOAD_DIR / file_path.replace("/uploads/", ""))

    path = Path(file_path)
    if path.exists() and path.is_file():
        path.unlink()
        return True
    return False
