"""CRUD operations for objectives."""

from typing import List, Optional
from datetime import datetime, timezone

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.models.objective import Objective, ObjectiveKPILink
from app.models.kpi import KPI
from app.schemas.objective import ObjectiveCreate, ObjectiveUpdate


class ObjectiveCRUD:
    """CRUD operations for objectives with hierarchy support."""

    def __init__(self):
        self.model = Objective

    def create(self, db: Session, *, obj_in: ObjectiveCreate, created_by: int) -> Objective:
        """Create new objective."""
        obj_data = obj_in.model_dump()
        obj_data["created_by"] = created_by
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, objective_id: int) -> Optional[Objective]:
        """Get objective by ID."""
        return db.query(self.model).filter(self.model.id == objective_id).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None,
        level: Optional[str] = None,
        year: Optional[int] = None,
        quarter: Optional[str] = None,
        status: Optional[str] = None,
        department: Optional[str] = None,
    ) -> List[Objective]:
        """Get multiple objectives with filters."""
        query = db.query(self.model)

        if owner_id is not None:
            query = query.filter(self.model.owner_id == owner_id)
        if level is not None:
            query = query.filter(self.model.level == level)
        if year is not None:
            query = query.filter(self.model.year == year)
        if quarter is not None:
            query = query.filter(self.model.quarter == quarter)
        if status is not None:
            query = query.filter(self.model.status == status)
        if department is not None:
            query = query.filter(self.model.department == department)

        return query.offset(skip).limit(limit).all()

    def update(
        self, db: Session, *, db_obj: Objective, obj_in: ObjectiveUpdate
    ) -> Objective:
        """Update objective."""
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db_obj.updated_at = datetime.now(timezone.utc)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, objective_id: int) -> Objective:
        """Delete objective (cascades to children and links)."""
        obj = db.query(self.model).get(objective_id)
        db.delete(obj)
        db.commit()
        return obj

    # Hierarchy operations
    def get_children(self, db: Session, parent_id: int) -> List[Objective]:
        """Get direct children of an objective."""
        return db.query(self.model).filter(self.model.parent_id == parent_id).all()

    def get_ancestors(self, db: Session, objective_id: int) -> List[Objective]:
        """Get all ancestors (parent chain) of an objective."""
        ancestors = []
        current = self.get(db, objective_id)

        while current and current.parent_id:
            parent = self.get(db, current.parent_id)
            if parent:
                ancestors.append(parent)
                current = parent
            else:
                break

        return list(reversed(ancestors))  # Return from top to bottom

    def get_tree(self, db: Session, root_id: Optional[int] = None) -> List[Objective]:
        """
        Get full tree structure.
        If root_id is provided, returns subtree from that root.
        If root_id is None, returns all top-level objectives and their trees.
        """
        if root_id:
            root = self.get(db, root_id)
            if root:
                return self._build_tree_recursive(db, root)
            return []
        else:
            # Get all top-level objectives (no parent)
            roots = db.query(self.model).filter(self.model.parent_id.is_(None)).all()
            result = []
            for root in roots:
                result.append(self._build_tree_recursive(db, root))
            return result

    def _build_tree_recursive(self, db: Session, node: Objective) -> Objective:
        """Build tree recursively (internal helper)."""
        # Load children
        node.children = self.get_children(db, node.id)

        # Recursively build subtrees
        for child in node.children:
            self._build_tree_recursive(db, child)

        return node

    def move(
        self, db: Session, *, objective_id: int, new_parent_id: Optional[int]
    ) -> Objective:
        """Move objective to a different parent."""
        obj = self.get(db, objective_id)
        if not obj:
            return None

        # Validate no circular reference
        if new_parent_id:
            if objective_id == new_parent_id:
                raise ValueError("Cannot move objective to itself")

            ancestors = self.get_ancestors(db, new_parent_id)
            if any(ancestor.id == objective_id for ancestor in ancestors):
                raise ValueError("Cannot create circular reference")

        obj.parent_id = new_parent_id
        obj.updated_at = datetime.now(timezone.utc)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    # KPI linking operations
    def link_kpi(
        self, db: Session, *, objective_id: int, kpi_id: int, weight: float = 1.0
    ) -> ObjectiveKPILink:
        """Link a KPI to an objective."""
        # Check if link already exists
        existing = (
            db.query(ObjectiveKPILink)
            .filter(
                ObjectiveKPILink.objective_id == objective_id,
                ObjectiveKPILink.kpi_id == kpi_id,
            )
            .first()
        )

        if existing:
            # Update weight if already exists
            existing.weight = weight
            db.commit()
            db.refresh(existing)
            return existing

        # Create new link
        link = ObjectiveKPILink(
            objective_id=objective_id, kpi_id=kpi_id, weight=weight
        )
        db.add(link)
        db.commit()
        db.refresh(link)
        return link

    def unlink_kpi(self, db: Session, *, objective_id: int, kpi_id: int) -> bool:
        """Unlink a KPI from an objective."""
        link = (
            db.query(ObjectiveKPILink)
            .filter(
                ObjectiveKPILink.objective_id == objective_id,
                ObjectiveKPILink.kpi_id == kpi_id,
            )
            .first()
        )

        if link:
            db.delete(link)
            db.commit()
            return True
        return False

    def get_linked_kpis(self, db: Session, objective_id: int) -> List[KPI]:
        """Get all KPIs linked to an objective."""
        links = (
            db.query(ObjectiveKPILink)
            .filter(ObjectiveKPILink.objective_id == objective_id)
            .all()
        )
        return [link.kpi for link in links]

    # Progress calculation
    def calculate_progress(self, db: Session, objective_id: int) -> float:
        """
        Calculate progress for an objective.

        Logic:
        1. If has children objectives → average of children progress
        2. Else if has linked KPIs → weighted average of KPI progress
        3. Else → manual progress (already set)
        """
        obj = self.get(db, objective_id)
        if not obj:
            return 0.0

        # Check for children
        children = self.get_children(db, objective_id)
        if children:
            # Average of children progress
            total_progress = sum(child.progress_percentage for child in children)
            return total_progress / len(children) if children else 0.0

        # Check for linked KPIs
        links = (
            db.query(ObjectiveKPILink)
            .filter(ObjectiveKPILink.objective_id == objective_id)
            .all()
        )

        if links:
            # Weighted average of KPI progress
            total_weight = sum(link.weight for link in links)
            if total_weight == 0:
                return 0.0

            weighted_progress = sum(
                (link.kpi.progress_percentage or 0) * link.weight for link in links
            )
            return weighted_progress / total_weight

        # No children or KPIs, return current manual progress
        return obj.progress_percentage

    def recalculate_progress(self, db: Session, objective_id: int) -> Objective:
        """Recalculate and update objective progress."""
        obj = self.get(db, objective_id)
        if not obj:
            return None

        new_progress = self.calculate_progress(db, objective_id)
        obj.progress_percentage = new_progress
        obj.updated_at = datetime.now(timezone.utc)
        db.add(obj)
        db.commit()
        db.refresh(obj)

        # Recursively update parent progress
        if obj.parent_id:
            self.recalculate_progress(db, obj.parent_id)

        return obj

    # Statistics
    def get_stats(self, db: Session, **filters) -> dict:
        """Get statistics for objectives."""
        query = db.query(self.model)

        # Apply filters
        if "owner_id" in filters and filters["owner_id"]:
            query = query.filter(self.model.owner_id == filters["owner_id"])
        if "year" in filters and filters["year"]:
            query = query.filter(self.model.year == filters["year"])
        if "department" in filters and filters["department"]:
            query = query.filter(self.model.department == filters["department"])

        total = query.count()

        # By level
        by_level = (
            query.with_entities(self.model.level, func.count(self.model.id))
            .group_by(self.model.level)
            .all()
        )

        # By status
        by_status = (
            query.with_entities(self.model.status, func.count(self.model.id))
            .group_by(self.model.status)
            .all()
        )

        # Average progress
        avg_progress = (
            query.with_entities(func.avg(self.model.progress_percentage))
            .scalar()
        )

        return {
            "total": total,
            "by_level": {level: count for level, count in by_level},
            "by_status": {status: count for status, count in by_status},
            "average_progress": float(avg_progress) if avg_progress else 0.0,
        }


# Create singleton instance
objective_crud = ObjectiveCRUD()
