"""KPI API endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.schemas.kpi import (
    KPICreate,
    KPIUpdate,
    KPIResponse,
    KPIListResponse,
    KPISubmit,
    KPIApprove,
    KPIReject,
    KPIStatistics,
    DashboardStatistics,
)
from app.schemas.objective import ObjectiveKPILinkResponse
from app.services.kpi import kpi_service

router = APIRouter()


@router.get("/statistics", response_model=KPIStatistics)
def get_kpi_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get KPI statistics.

    - Employees: Only their own statistics
    - Managers/Admins: Overall statistics
    """
    return kpi_service.get_statistics(db, current_user=current_user)


@router.get("/dashboard", response_model=DashboardStatistics)
def get_dashboard_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get dashboard statistics including quarterly breakdown.
    """
    return kpi_service.get_dashboard_statistics(db, current_user=current_user)


@router.get("/pending", response_model=KPIListResponse)
def get_pending_approvals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get KPIs pending approval (managers only).
    """
    return kpi_service.get_pending_approvals(
        db, current_user=current_user, skip=skip, limit=limit
    )


@router.get("", response_model=KPIListResponse)
def get_kpis(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    user_id: Optional[int] = Query(None),
    year: Optional[int] = Query(None, ge=2000, le=2100),
    quarter: Optional[str] = Query(None, pattern="^Q[1-4]$"),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get list of KPIs with filters.

    - Employees: Only their own KPIs
    - Managers/Admins: Can filter by user_id or see all

    Filters:
    - user_id: Filter by user ID (managers/admins only)
    - year: Filter by year
    - quarter: Filter by quarter (Q1, Q2, Q3, Q4)
    - status: Filter by status (draft, submitted, approved, rejected)
    - search: Search in title and description
    """
    return kpi_service.get_kpis(
        db,
        current_user=current_user,
        skip=skip,
        limit=limit,
        user_id=user_id,
        year=year,
        quarter=quarter,
        status=status,
        search=search,
    )


@router.post("", response_model=KPIResponse, status_code=201)
def create_kpi(
    kpi_in: KPICreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new KPI.

    Creates a KPI in 'draft' status for the current user.
    """
    return kpi_service.create_kpi(db, kpi_in=kpi_in, current_user=current_user)


@router.get("/{kpi_id}", response_model=KPIResponse)
def get_kpi(
    kpi_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get a single KPI by ID.

    - Employees: Can only view their own KPIs
    - Managers/Admins: Can view all KPIs
    """
    return kpi_service.get_kpi(db, kpi_id=kpi_id, current_user=current_user)


@router.put("/{kpi_id}", response_model=KPIResponse)
def update_kpi(
    kpi_id: int,
    kpi_in: KPIUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a KPI.

    - Can only update own KPIs
    - Can only update draft or rejected KPIs
    """
    return kpi_service.update_kpi(db, kpi_id=kpi_id, kpi_in=kpi_in, current_user=current_user)


@router.delete("/{kpi_id}")
def delete_kpi(
    kpi_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a KPI.

    - Can only delete own KPIs
    - Can only delete draft KPIs
    """
    return kpi_service.delete_kpi(db, kpi_id=kpi_id, current_user=current_user)


@router.post("/{kpi_id}/submit", response_model=KPIResponse)
def submit_kpi(
    kpi_id: int,
    submit_data: KPISubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Submit a KPI for approval.

    Changes status from 'draft' to 'submitted'.
    """
    return kpi_service.submit_kpi(
        db, kpi_id=kpi_id, submit_data=submit_data, current_user=current_user
    )


@router.post("/{kpi_id}/approve", response_model=KPIResponse)
def approve_kpi(
    kpi_id: int,
    approve_data: KPIApprove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Approve a KPI (managers only).

    Changes status from 'submitted' to 'approved'.
    """
    return kpi_service.approve_kpi(
        db, kpi_id=kpi_id, approve_data=approve_data, current_user=current_user
    )


@router.post("/{kpi_id}/reject", response_model=KPIResponse)
def reject_kpi(
    kpi_id: int,
    reject_data: KPIReject,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Reject a KPI (managers only).

    Changes status from 'submitted' to 'rejected'.
    Requires a reason for rejection.
    """
    return kpi_service.reject_kpi(
        db, kpi_id=kpi_id, reject_data=reject_data, current_user=current_user
    )


@router.get("/{kpi_id}/objectives", response_model=list[ObjectiveKPILinkResponse])
def get_kpi_objectives(
    kpi_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get all objectives linked to this KPI.

    Returns list of objectives with their link information (weight).
    """
    from app.crud.objective import objective_crud
    return objective_crud.get_objectives_by_kpi(db, kpi_id=kpi_id)
