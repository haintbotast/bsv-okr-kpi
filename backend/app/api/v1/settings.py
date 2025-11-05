"""System settings API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_admin
from app.models.user import User
from app.schemas.system import CategoryCreate, CategoryResponse
from app.crud.system import system_settings

router = APIRouter()


@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db)
):
    """Get list of available KPI categories."""
    categories = system_settings.get_categories(db)
    return [{"name": cat} for cat in categories]


@router.post("/categories", response_model=List[CategoryResponse], status_code=status.HTTP_201_CREATED)
def add_category(
    category_in: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Add a new KPI category (admin only)."""
    # Check if category already exists
    categories = system_settings.get_categories(db)
    if category_in.name in categories:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists"
        )

    # Add category
    updated_categories = system_settings.add_category(db, category_in.name)
    return [{"name": cat} for cat in updated_categories]


@router.delete("/categories/{category_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete a KPI category (admin only)."""
    categories = system_settings.get_categories(db)
    if category_name not in categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    system_settings.remove_category(db, category_name)
    return None
