"""KPI Template API endpoints."""

from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, require_admin
from app.models.user import User
from app.schemas.kpi import (
    KPITemplateCreate,
    KPITemplateUpdate,
    KPITemplateResponse,
)
from app.services.kpi import kpi_template_service

router = APIRouter()


@router.get("", response_model=List[KPITemplateResponse])
def get_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    is_active: Optional[bool] = Query(True),
    role: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get list of KPI templates.

    Filters:
    - is_active: Show only active templates (default: true)
    - role: Filter by role (admin, manager, employee)
    - category: Filter by category
    """
    templates = kpi_template_service.get_templates(
        db, skip=skip, limit=limit, is_active=is_active, role=role, category=category
    )
    return [KPITemplateResponse.model_validate(t) for t in templates]


@router.post("", response_model=KPITemplateResponse, status_code=201)
def create_template(
    template_in: KPITemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Create a new KPI template (admin only).
    """
    template = kpi_template_service.create_template(
        db, template_in=template_in, current_user=current_user
    )
    return KPITemplateResponse.model_validate(template)


@router.get("/{template_id}", response_model=KPITemplateResponse)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get a single template by ID.
    """
    template = kpi_template_service.get_template(db, template_id=template_id)
    return KPITemplateResponse.model_validate(template)


@router.put("/{template_id}", response_model=KPITemplateResponse)
def update_template(
    template_id: int,
    template_in: KPITemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Update a template (admin only).
    """
    template = kpi_template_service.update_template(
        db, template_id=template_id, template_in=template_in, current_user=current_user
    )
    return KPITemplateResponse.model_validate(template)


@router.delete("/{template_id}")
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Delete a template (admin only).

    This is a soft delete - sets is_active to False.
    """
    return kpi_template_service.delete_template(
        db, template_id=template_id, current_user=current_user
    )
