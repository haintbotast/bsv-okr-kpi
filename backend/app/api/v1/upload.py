"""File upload API endpoints."""

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict

from app.database import get_db
from app.models.user import User
from app.crud.user import user as user_crud
from app.api.deps import get_current_active_user, require_admin
from app.utils.file_upload import save_avatar, delete_file, ensure_upload_dirs


router = APIRouter()


# Ensure upload directories exist on module load
ensure_upload_dirs()


@router.post("/avatar", response_model=Dict[str, str])
async def upload_own_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Upload avatar for current user.

    - **file**: Image file (jpg, png, gif, webp, max 5MB)

    Returns the avatar URL.
    """
    # Delete old avatar if exists
    if current_user.avatar_url:
        delete_file(current_user.avatar_url)

    # Save new avatar
    avatar_url = await save_avatar(file)

    # Update user in database
    current_user.avatar_url = avatar_url
    db.commit()
    db.refresh(current_user)

    return {"avatar_url": avatar_url}


@router.post("/avatar/{user_id}", response_model=Dict[str, str])
async def upload_user_avatar(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Upload avatar for any user (admin only).

    - **user_id**: Target user ID
    - **file**: Image file (jpg, png, gif, webp, max 5MB)

    Returns the avatar URL.
    """
    # Get target user
    target_user = user_crud.get(db, user_id=user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Delete old avatar if exists
    if target_user.avatar_url:
        delete_file(target_user.avatar_url)

    # Save new avatar
    avatar_url = await save_avatar(file)

    # Update user in database
    target_user.avatar_url = avatar_url
    db.commit()
    db.refresh(target_user)

    return {"avatar_url": avatar_url}


@router.delete("/avatar")
async def delete_own_avatar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete current user's avatar."""
    if not current_user.avatar_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No avatar to delete"
        )

    # Delete file
    delete_file(current_user.avatar_url)

    # Update database
    current_user.avatar_url = None
    db.commit()

    return {"message": "Avatar deleted successfully"}


@router.delete("/avatar/{user_id}")
async def delete_user_avatar(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete any user's avatar (admin only)."""
    # Get target user
    target_user = user_crud.get(db, user_id=user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not target_user.avatar_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User has no avatar to delete"
        )

    # Delete file
    delete_file(target_user.avatar_url)

    # Update database
    target_user.avatar_url = None
    db.commit()

    return {"message": "Avatar deleted successfully"}
