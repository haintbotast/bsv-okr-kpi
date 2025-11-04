"""KPI CRUD operations."""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from datetime import datetime, timezone

from app.models.kpi import KPI, KPITemplate, KPIEvidence, KPIComment, KPIHistory
from app.schemas.kpi import (
    KPICreate,
    KPIUpdate,
    KPITemplateCreate,
    KPITemplateUpdate,
    KPIEvidenceCreate,
    KPICommentCreate,
)


# ============================================================================
# KPI Template CRUD
# ============================================================================

class CRUDKPITemplate:
    """CRUD operations for KPI templates."""

    def get(self, db: Session, template_id: int) -> Optional[KPITemplate]:
        """Get a KPI template by ID."""
        return db.query(KPITemplate).filter(KPITemplate.id == template_id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        role: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[KPITemplate]:
        """Get multiple KPI templates with filters."""
        query = db.query(KPITemplate)

        if is_active is not None:
            query = query.filter(KPITemplate.is_active == is_active)
        if role:
            query = query.filter(KPITemplate.role == role)
        if category:
            query = query.filter(KPITemplate.category == category)

        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: KPITemplateCreate, created_by: int) -> KPITemplate:
        """Create a new KPI template."""
        db_obj = KPITemplate(
            **obj_in.model_dump(),
            created_by=created_by,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: KPITemplate, obj_in: KPITemplateUpdate
    ) -> KPITemplate:
        """Update a KPI template."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, template_id: int) -> bool:
        """Delete a KPI template (soft delete by marking inactive)."""
        db_obj = self.get(db, template_id=template_id)
        if db_obj:
            db_obj.is_active = False
            db.commit()
            return True
        return False


# ============================================================================
# KPI CRUD
# ============================================================================

class CRUDKPI:
    """CRUD operations for KPIs."""

    def get(self, db: Session, kpi_id: int) -> Optional[KPI]:
        """Get a KPI by ID."""
        return db.query(KPI).filter(KPI.id == kpi_id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
        year: Optional[int] = None,
        quarter: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
    ) -> tuple[List[KPI], int]:
        """Get multiple KPIs with filters and return (items, total_count)."""
        query = db.query(KPI)

        # Apply filters
        if user_id:
            query = query.filter(KPI.user_id == user_id)
        if year:
            query = query.filter(KPI.year == year)
        if quarter:
            query = query.filter(KPI.quarter == quarter)
        if status:
            query = query.filter(KPI.status == status)
        if search:
            search_filter = or_(
                KPI.title.ilike(f"%{search}%"),
                KPI.description.ilike(f"%{search}%"),
            )
            query = query.filter(search_filter)

        # Get total count before pagination
        total = query.count()

        # Apply pagination and ordering
        items = query.order_by(KPI.created_at.desc()).offset(skip).limit(limit).all()

        return items, total

    def get_pending_approvals(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> tuple[List[KPI], int]:
        """Get KPIs pending approval."""
        query = db.query(KPI).filter(KPI.status == "submitted")
        total = query.count()
        items = query.order_by(KPI.submitted_at.desc()).offset(skip).limit(limit).all()
        return items, total

    def create(self, db: Session, *, obj_in: KPICreate, user_id: int) -> KPI:
        """Create a new KPI."""
        db_obj = KPI(
            **obj_in.model_dump(),
            user_id=user_id,
            status="draft",
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Create history record
        self._create_history(
            db,
            kpi_id=db_obj.id,
            user_id=user_id,
            action="created",
            new_value=f"Created KPI: {db_obj.title}",
        )

        return db_obj

    def update(self, db: Session, *, db_obj: KPI, obj_in: KPIUpdate, user_id: int) -> KPI:
        """Update a KPI."""
        update_data = obj_in.model_dump(exclude_unset=True)

        # Track changes for history
        changes = []
        for field, value in update_data.items():
            old_value = getattr(db_obj, field)
            if old_value != value:
                changes.append(f"{field}: {old_value} → {value}")
                setattr(db_obj, field, value)

        if changes:
            db.commit()
            db.refresh(db_obj)

            # Create history record
            self._create_history(
                db,
                kpi_id=db_obj.id,
                user_id=user_id,
                action="updated",
                old_value="; ".join([c.split(":")[0] for c in changes]),
                new_value="; ".join(changes),
            )

        return db_obj

    def delete(self, db: Session, *, kpi_id: int, user_id: int) -> bool:
        """Delete a KPI (only if in draft status)."""
        db_obj = self.get(db, kpi_id=kpi_id)
        if db_obj and db_obj.status == "draft":
            self._create_history(
                db,
                kpi_id=db_obj.id,
                user_id=user_id,
                action="deleted",
                old_value=f"Deleted KPI: {db_obj.title}",
            )
            db.delete(db_obj)
            db.commit()
            return True
        return False

    def submit_for_approval(self, db: Session, *, kpi_id: int, user_id: int) -> Optional[KPI]:
        """Submit a KPI for approval."""
        db_obj = self.get(db, kpi_id=kpi_id)
        if db_obj and db_obj.status == "draft":
            db_obj.status = "submitted"
            db_obj.submitted_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(db_obj)

            self._create_history(
                db,
                kpi_id=db_obj.id,
                user_id=user_id,
                action="submitted",
                new_value="Submitted for approval",
            )

            return db_obj
        return None

    def approve(
        self, db: Session, *, kpi_id: int, approver_id: int, comment: Optional[str] = None
    ) -> Optional[KPI]:
        """Approve a KPI."""
        db_obj = self.get(db, kpi_id=kpi_id)
        if db_obj and db_obj.status == "submitted":
            db_obj.status = "approved"
            db_obj.approved_at = datetime.now(timezone.utc)
            db_obj.approved_by = approver_id
            db.commit()
            db.refresh(db_obj)

            self._create_history(
                db,
                kpi_id=db_obj.id,
                user_id=approver_id,
                action="approved",
                new_value=comment or "Approved",
            )

            if comment:
                self._create_comment(db, kpi_id=kpi_id, user_id=approver_id, comment=comment)

            return db_obj
        return None

    def reject(
        self, db: Session, *, kpi_id: int, approver_id: int, reason: str
    ) -> Optional[KPI]:
        """Reject a KPI."""
        db_obj = self.get(db, kpi_id=kpi_id)
        if db_obj and db_obj.status == "submitted":
            db_obj.status = "rejected"
            db.commit()
            db.refresh(db_obj)

            self._create_history(
                db,
                kpi_id=db_obj.id,
                user_id=approver_id,
                action="rejected",
                new_value=f"Rejected: {reason}",
            )

            self._create_comment(db, kpi_id=kpi_id, user_id=approver_id, comment=reason)

            return db_obj
        return None

    def get_statistics(self, db: Session, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get KPI statistics."""
        query = db.query(KPI)
        if user_id:
            query = query.filter(KPI.user_id == user_id)

        total_kpis = query.count()
        draft = query.filter(KPI.status == "draft").count()
        submitted = query.filter(KPI.status == "submitted").count()
        approved = query.filter(KPI.status == "approved").count()
        rejected = query.filter(KPI.status == "rejected").count()

        # Calculate average progress
        avg_progress = db.query(func.avg(KPI.progress_percentage)).filter(
            KPI.progress_percentage.isnot(None)
        )
        if user_id:
            avg_progress = avg_progress.filter(KPI.user_id == user_id)
        avg_progress = avg_progress.scalar() or 0.0

        # Calculate completion rate (approved KPIs)
        completion_rate = (approved / total_kpis * 100) if total_kpis > 0 else 0.0

        return {
            "total_kpis": total_kpis,
            "draft": draft,
            "submitted": submitted,
            "approved": approved,
            "rejected": rejected,
            "average_progress": round(avg_progress, 2),
            "completion_rate": round(completion_rate, 2),
        }

    def _create_history(
        self,
        db: Session,
        *,
        kpi_id: int,
        user_id: int,
        action: str,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
    ) -> KPIHistory:
        """Create a history record."""
        history = KPIHistory(
            kpi_id=kpi_id,
            user_id=user_id,
            action=action,
            old_value=old_value,
            new_value=new_value,
        )
        db.add(history)
        db.commit()
        return history

    def _create_comment(
        self, db: Session, *, kpi_id: int, user_id: int, comment: str
    ) -> KPIComment:
        """Create a comment."""
        comment_obj = KPIComment(
            kpi_id=kpi_id,
            user_id=user_id,
            comment=comment,
        )
        db.add(comment_obj)
        db.commit()
        return comment_obj


# ============================================================================
# KPI Evidence CRUD
# ============================================================================

class CRUDKPIEvidence:
    """CRUD operations for KPI evidence."""

    def get(self, db: Session, evidence_id: int) -> Optional[KPIEvidence]:
        """Get evidence by ID."""
        return db.query(KPIEvidence).filter(KPIEvidence.id == evidence_id).first()

    def get_by_kpi(self, db: Session, kpi_id: int) -> List[KPIEvidence]:
        """Get all evidence for a KPI."""
        return db.query(KPIEvidence).filter(KPIEvidence.kpi_id == kpi_id).all()

    def create(
        self, db: Session, *, obj_in: KPIEvidenceCreate, kpi_id: int, uploaded_by: int
    ) -> KPIEvidence:
        """Create new evidence."""
        db_obj = KPIEvidence(
            **obj_in.model_dump(),
            kpi_id=kpi_id,
            uploaded_by=uploaded_by,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, evidence_id: int) -> bool:
        """Delete evidence."""
        db_obj = self.get(db, evidence_id=evidence_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False


# ============================================================================
# KPI Comment CRUD
# ============================================================================

class CRUDKPIComment:
    """CRUD operations for KPI comments."""

    def get(self, db: Session, comment_id: int) -> Optional[KPIComment]:
        """Get comment by ID."""
        return db.query(KPIComment).filter(KPIComment.id == comment_id).first()

    def get_by_kpi(self, db: Session, kpi_id: int) -> List[KPIComment]:
        """Get all comments for a KPI."""
        return (
            db.query(KPIComment)
            .filter(KPIComment.kpi_id == kpi_id)
            .order_by(KPIComment.created_at.desc())
            .all()
        )

    def create(
        self, db: Session, *, obj_in: KPICommentCreate, kpi_id: int, user_id: int
    ) -> KPIComment:
        """Create a new comment."""
        db_obj = KPIComment(
            **obj_in.model_dump(),
            kpi_id=kpi_id,
            user_id=user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, comment_id: int) -> bool:
        """Delete a comment."""
        db_obj = self.get(db, comment_id=comment_id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False


# ============================================================================
# Instances
# ============================================================================

kpi_template_crud = CRUDKPITemplate()
kpi_crud = CRUDKPI()
kpi_evidence_crud = CRUDKPIEvidence()
kpi_comment_crud = CRUDKPIComment()
