"""Comment API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.schemas.kpi import KPICommentCreate, KPICommentResponse
from app.crud.kpi_comment import kpi_comment_crud
from app.crud.kpi import kpi_crud

router = APIRouter()


@router.post("/kpis/{kpi_id}/comments", response_model=KPICommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    kpi_id: int,
    comment_in: KPICommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a comment on a KPI.

    **Args:**
    - kpi_id: KPI ID to comment on
    - comment_in: Comment data

    **Returns:**
    - Created comment
    """
    # Verify KPI exists
    kpi = kpi_crud.get(db, kpi_id=kpi_id)
    if not kpi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KPI not found"
        )

    # Check permissions: employees can only comment on their own KPIs
    if current_user.role == "employee" and kpi.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only comment on your own KPIs"
        )

    comment = kpi_comment_crud.create(
        db,
        kpi_id=kpi_id,
        comment_in=comment_in,
        user_id=current_user.id
    )

    return comment


@router.get("/kpis/{kpi_id}/comments", response_model=List[KPICommentResponse])
def list_comments(
    kpi_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all comments for a KPI.

    **Args:**
    - kpi_id: KPI ID
    - skip: Number of comments to skip (pagination)
    - limit: Maximum number of comments to return

    **Returns:**
    - List of comments
    """
    # Verify KPI exists
    kpi = kpi_crud.get(db, kpi_id=kpi_id)
    if not kpi:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="KPI not found"
        )

    # Check permissions
    if current_user.role == "employee" and kpi.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view comments on your own KPIs"
        )

    comments = kpi_comment_crud.get_by_kpi(db, kpi_id=kpi_id, skip=skip, limit=limit)
    return comments


@router.put("/comments/{comment_id}", response_model=KPICommentResponse)
def update_comment(
    comment_id: int,
    comment_text: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a comment.

    **Security:**
    - Only the comment author can update it

    **Args:**
    - comment_id: Comment ID
    - comment_text: New comment text

    **Returns:**
    - Updated comment
    """
    # Get comment
    comment = kpi_comment_crud.get(db, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    # Check ownership
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own comments"
        )

    updated_comment = kpi_comment_crud.update(
        db,
        comment_id=comment_id,
        comment_text=comment_text
    )

    return updated_comment


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a comment.

    **Security:**
    - Only the comment author or admin can delete it

    **Args:**
    - comment_id: Comment ID to delete
    """
    # Get comment
    comment = kpi_comment_crud.get(db, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    # Check permissions: only author or admin can delete
    if comment.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments"
        )

    kpi_comment_crud.delete(db, comment_id=comment_id)
    return None
