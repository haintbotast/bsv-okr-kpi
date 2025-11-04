"""KPI business logic service."""

from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.kpi import KPI, KPITemplate
from app.schemas.kpi import (
    KPICreate,
    KPIUpdate,
    KPIResponse,
    KPIListResponse,
    KPITemplateCreate,
    KPITemplateUpdate,
    KPISubmit,
    KPIApprove,
    KPIReject,
    KPIStatistics,
    DashboardStatistics,
)
from app.crud.kpi import kpi_crud, kpi_template_crud
import math


class KPIService:
    """KPI service for business logic."""

    def get_kpi(self, db: Session, kpi_id: int, current_user: User) -> KPIResponse:
        """Get a single KPI."""
        kpi = kpi_crud.get(db, kpi_id=kpi_id)
        if not kpi:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="KPI not found",
            )

        # Check permissions
        if not self._can_view_kpi(kpi, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this KPI",
            )

        return KPIResponse.model_validate(kpi)

    def get_kpis(
        self,
        db: Session,
        current_user: User,
        *,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
        year: Optional[int] = None,
        quarter: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> KPIListResponse:
        """Get list of KPIs with filters."""
        # If employee, only show their own KPIs
        if current_user.role == "employee":
            user_id = current_user.id

        items, total = kpi_crud.get_multi(
            db,
            skip=skip,
            limit=limit,
            user_id=user_id,
            year=year,
            quarter=quarter,
            status=status,
            search=search,
        )

        page = (skip // limit) + 1 if limit > 0 else 1
        total_pages = math.ceil(total / limit) if limit > 0 else 1

        return KPIListResponse(
            items=[KPIResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=limit,
            total_pages=total_pages,
        )

    def get_pending_approvals(
        self, db: Session, current_user: User, *, skip: int = 0, limit: int = 100
    ) -> KPIListResponse:
        """Get KPIs pending approval (managers only)."""
        if current_user.role not in ["admin", "manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only managers can view pending approvals",
            )

        items, total = kpi_crud.get_pending_approvals(db, skip=skip, limit=limit)

        page = (skip // limit) + 1 if limit > 0 else 1
        total_pages = math.ceil(total / limit) if limit > 0 else 1

        return KPIListResponse(
            items=[KPIResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=limit,
            total_pages=total_pages,
        )

    def create_kpi(self, db: Session, kpi_in: KPICreate, current_user: User) -> KPIResponse:
        """Create a new KPI."""
        # Validate template if provided
        if kpi_in.template_id:
            template = kpi_template_crud.get(db, template_id=kpi_in.template_id)
            if not template or not template.is_active:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Template not found or inactive",
                )

        kpi = kpi_crud.create(db, obj_in=kpi_in, user_id=current_user.id)
        return KPIResponse.model_validate(kpi)

    def update_kpi(
        self, db: Session, kpi_id: int, kpi_in: KPIUpdate, current_user: User
    ) -> KPIResponse:
        """Update a KPI."""
        kpi = kpi_crud.get(db, kpi_id=kpi_id)
        if not kpi:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="KPI not found",
            )

        # Check permissions
        if not self._can_edit_kpi(kpi, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to edit this KPI",
            )

        # Can only edit draft or rejected KPIs
        if kpi.status not in ["draft", "rejected"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot edit KPI with status: {kpi.status}",
            )

        kpi = kpi_crud.update(db, db_obj=kpi, obj_in=kpi_in, user_id=current_user.id)
        return KPIResponse.model_validate(kpi)

    def delete_kpi(self, db: Session, kpi_id: int, current_user: User) -> dict:
        """Delete a KPI (draft only)."""
        kpi = kpi_crud.get(db, kpi_id=kpi_id)
        if not kpi:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="KPI not found",
            )

        # Check permissions
        if not self._can_edit_kpi(kpi, current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this KPI",
            )

        # Can only delete draft KPIs
        if kpi.status != "draft":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only delete draft KPIs",
            )

        success = kpi_crud.delete(db, kpi_id=kpi_id, user_id=current_user.id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to delete KPI",
            )

        return {"message": "KPI deleted successfully"}

    def submit_kpi(
        self, db: Session, kpi_id: int, submit_data: KPISubmit, current_user: User
    ) -> KPIResponse:
        """Submit a KPI for approval."""
        kpi = kpi_crud.get(db, kpi_id=kpi_id)
        if not kpi:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="KPI not found",
            )

        # Check permissions
        if kpi.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to submit this KPI",
            )

        kpi = kpi_crud.submit_for_approval(db, kpi_id=kpi_id, user_id=current_user.id)
        if not kpi:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot submit KPI in current status",
            )

        return KPIResponse.model_validate(kpi)

    def approve_kpi(
        self, db: Session, kpi_id: int, approve_data: KPIApprove, current_user: User
    ) -> KPIResponse:
        """Approve a KPI (managers only)."""
        if current_user.role not in ["admin", "manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only managers can approve KPIs",
            )

        kpi = kpi_crud.get(db, kpi_id=kpi_id)
        if not kpi:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="KPI not found",
            )

        kpi = kpi_crud.approve(
            db, kpi_id=kpi_id, approver_id=current_user.id, comment=approve_data.comment
        )
        if not kpi:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot approve KPI in current status",
            )

        return KPIResponse.model_validate(kpi)

    def reject_kpi(
        self, db: Session, kpi_id: int, reject_data: KPIReject, current_user: User
    ) -> KPIResponse:
        """Reject a KPI (managers only)."""
        if current_user.role not in ["admin", "manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only managers can reject KPIs",
            )

        kpi = kpi_crud.get(db, kpi_id=kpi_id)
        if not kpi:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="KPI not found",
            )

        kpi = kpi_crud.reject(
            db, kpi_id=kpi_id, approver_id=current_user.id, reason=reject_data.reason
        )
        if not kpi:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot reject KPI in current status",
            )

        return KPIResponse.model_validate(kpi)

    def get_statistics(self, db: Session, current_user: User) -> KPIStatistics:
        """Get KPI statistics."""
        # Employees only see their own stats
        user_id = current_user.id if current_user.role == "employee" else None
        stats = kpi_crud.get_statistics(db, user_id=user_id)
        return KPIStatistics(**stats)

    def get_dashboard_statistics(self, db: Session, current_user: User) -> DashboardStatistics:
        """Get dashboard statistics."""
        # Get overall stats
        if current_user.role == "employee":
            stats = kpi_crud.get_statistics(db, user_id=current_user.id)
            my_kpis = stats["total_kpis"]
        else:
            stats = kpi_crud.get_statistics(db)
            my_kpis = kpi_crud.get_statistics(db, user_id=current_user.id)["total_kpis"]

        # Get quarterly stats (placeholder for now)
        quarterly_stats = []

        return DashboardStatistics(
            total_kpis=stats["total_kpis"],
            pending_approval=stats["submitted"],
            approved=stats["approved"],
            rejected=stats["rejected"],
            my_kpis=my_kpis,
            average_progress=stats["average_progress"],
            quarterly_stats=quarterly_stats,
        )

    def _can_view_kpi(self, kpi: KPI, user: User) -> bool:
        """Check if user can view a KPI."""
        # Admins and managers can view all KPIs
        if user.role in ["admin", "manager"]:
            return True
        # Employees can only view their own KPIs
        return kpi.user_id == user.id

    def _can_edit_kpi(self, kpi: KPI, user: User) -> bool:
        """Check if user can edit a KPI."""
        # Only the owner can edit
        return kpi.user_id == user.id


class KPITemplateService:
    """KPI template service for business logic."""

    def get_template(self, db: Session, template_id: int) -> KPITemplate:
        """Get a single template."""
        template = kpi_template_crud.get(db, template_id=template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found",
            )
        return template

    def get_templates(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = True,
        role: Optional[str] = None,
        category: Optional[str] = None,
    ):
        """Get list of templates."""
        return kpi_template_crud.get_multi(
            db, skip=skip, limit=limit, is_active=is_active, role=role, category=category
        )

    def create_template(
        self, db: Session, template_in: KPITemplateCreate, current_user: User
    ) -> KPITemplate:
        """Create a new template (admin only)."""
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can create templates",
            )
        return kpi_template_crud.create(db, obj_in=template_in, created_by=current_user.id)

    def update_template(
        self, db: Session, template_id: int, template_in: KPITemplateUpdate, current_user: User
    ) -> KPITemplate:
        """Update a template (admin only)."""
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can update templates",
            )

        template = self.get_template(db, template_id=template_id)
        return kpi_template_crud.update(db, db_obj=template, obj_in=template_in)

    def delete_template(self, db: Session, template_id: int, current_user: User) -> dict:
        """Delete a template (admin only)."""
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can delete templates",
            )

        success = kpi_template_crud.delete(db, template_id=template_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found",
            )
        return {"message": "Template deleted successfully"}


# Service instances
kpi_service = KPIService()
kpi_template_service = KPITemplateService()
