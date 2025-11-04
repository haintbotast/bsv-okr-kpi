"""CRUD operations for KPI Comments."""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.kpi import KPIComment
from app.schemas.kpi import KPICommentCreate


class KPICommentCRUD:
    """CRUD operations for KPI Comments."""

    def create(
        self,
        db: Session,
        *,
        kpi_id: int,
        comment_in: KPICommentCreate,
        user_id: int
    ) -> KPIComment:
        """Create new comment for a KPI.

        Args:
            db: Database session
            kpi_id: KPI ID to attach comment to
            comment_in: Comment data
            user_id: User ID who created the comment

        Returns:
            Created KPIComment object
        """
        comment = KPIComment(
            kpi_id=kpi_id,
            user_id=user_id,
            comment=comment_in.comment
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    def get(self, db: Session, *, comment_id: int) -> Optional[KPIComment]:
        """Get comment by ID.

        Args:
            db: Database session
            comment_id: Comment ID

        Returns:
            KPIComment object or None
        """
        return db.query(KPIComment).filter(KPIComment.id == comment_id).first()

    def get_by_kpi(
        self,
        db: Session,
        *,
        kpi_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[KPIComment]:
        """Get all comments for a KPI.

        Args:
            db: Database session
            kpi_id: KPI ID
            skip: Number of comments to skip
            limit: Maximum number of comments to return

        Returns:
            List of KPIComment objects
        """
        return (
            db.query(KPIComment)
            .filter(KPIComment.kpi_id == kpi_id)
            .order_by(KPIComment.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
        self,
        db: Session,
        *,
        comment_id: int,
        comment_text: str
    ) -> Optional[KPIComment]:
        """Update comment text.

        Args:
            db: Database session
            comment_id: Comment ID
            comment_text: New comment text

        Returns:
            Updated KPIComment object or None
        """
        comment = self.get(db, comment_id=comment_id)
        if not comment:
            return None

        comment.comment = comment_text
        db.commit()
        db.refresh(comment)
        return comment

    def delete(self, db: Session, *, comment_id: int) -> bool:
        """Delete comment by ID.

        Args:
            db: Database session
            comment_id: Comment ID

        Returns:
            True if deleted, False if not found
        """
        comment = self.get(db, comment_id=comment_id)
        if not comment:
            return False

        db.delete(comment)
        db.commit()
        return True

    def count_by_kpi(self, db: Session, *, kpi_id: int) -> int:
        """Count comments for a KPI.

        Args:
            db: Database session
            kpi_id: KPI ID

        Returns:
            Number of comments
        """
        return db.query(KPIComment).filter(KPIComment.kpi_id == kpi_id).count()


# Create singleton instance
kpi_comment_crud = KPICommentCRUD()
