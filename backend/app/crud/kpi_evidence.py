"""CRUD operations for KPI Evidence."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.kpi import KPIEvidence
from app.schemas.kpi import KPIEvidenceCreate


class KPIEvidenceCRUD:
    """CRUD operations for KPI Evidence."""

    def create(
        self,
        db: Session,
        *,
        kpi_id: int,
        evidence_in: KPIEvidenceCreate,
        uploaded_by: int
    ) -> KPIEvidence:
        """Create new evidence for a KPI.

        Args:
            db: Database session
            kpi_id: KPI ID to attach evidence to
            evidence_in: Evidence data
            uploaded_by: User ID who uploaded the file

        Returns:
            Created KPIEvidence object
        """
        evidence = KPIEvidence(
            kpi_id=kpi_id,
            file_name=evidence_in.file_name,
            file_path=evidence_in.file_path,
            file_type=evidence_in.file_type,
            file_size=evidence_in.file_size,
            uploaded_by=uploaded_by,
            description=evidence_in.description
        )
        db.add(evidence)
        db.commit()
        db.refresh(evidence)
        return evidence

    def get(self, db: Session, *, evidence_id: int) -> Optional[KPIEvidence]:
        """Get evidence by ID.

        Args:
            db: Database session
            evidence_id: Evidence ID

        Returns:
            KPIEvidence object or None
        """
        return db.query(KPIEvidence).filter(KPIEvidence.id == evidence_id).first()

    def get_by_kpi(self, db: Session, *, kpi_id: int) -> List[KPIEvidence]:
        """Get all evidence for a KPI.

        Args:
            db: Database session
            kpi_id: KPI ID

        Returns:
            List of KPIEvidence objects
        """
        return (
            db.query(KPIEvidence)
            .filter(KPIEvidence.kpi_id == kpi_id)
            .order_by(KPIEvidence.uploaded_at.desc())
            .all()
        )

    def delete(self, db: Session, *, evidence_id: int) -> bool:
        """Delete evidence by ID.

        Args:
            db: Database session
            evidence_id: Evidence ID

        Returns:
            True if deleted, False if not found
        """
        evidence = self.get(db, evidence_id=evidence_id)
        if not evidence:
            return False

        db.delete(evidence)
        db.commit()
        return True

    def get_file_path(self, db: Session, *, evidence_id: int) -> Optional[str]:
        """Get file path for evidence.

        Args:
            db: Database session
            evidence_id: Evidence ID

        Returns:
            File path or None
        """
        evidence = self.get(db, evidence_id=evidence_id)
        return evidence.file_path if evidence else None


# Create singleton instance
kpi_evidence_crud = KPIEvidenceCRUD()
