"""CRUD operations for SystemSettings model."""

import json
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.system import SystemSettings
from app.schemas.system import SystemSettingsCreate, SystemSettingsUpdate


class CRUDSystemSettings:
    """CRUD operations for SystemSettings model."""

    def get(self, db: Session, key: str) -> Optional[SystemSettings]:
        """Get system setting by key."""
        return db.query(SystemSettings).filter(SystemSettings.key == key).first()

    def get_multi(self, db: Session) -> List[SystemSettings]:
        """Get all system settings."""
        return db.query(SystemSettings).all()

    def create(self, db: Session, *, obj_in: SystemSettingsCreate) -> SystemSettings:
        """Create new system setting."""
        db_obj = SystemSettings(
            key=obj_in.key,
            value=obj_in.value,
            description=obj_in.description,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: SystemSettings, obj_in: SystemSettingsUpdate
    ) -> SystemSettings:
        """Update system setting."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, key: str) -> bool:
        """Delete system setting by key."""
        setting = self.get(db, key=key)
        if not setting:
            return False
        db.delete(setting)
        db.commit()
        return True

    # Category-specific methods
    def get_categories(self, db: Session) -> List[str]:
        """Get list of KPI categories."""
        setting = self.get(db, key="kpi_categories")
        if not setting or not setting.value:
            return []
        try:
            return json.loads(setting.value)
        except json.JSONDecodeError:
            return []

    def set_categories(self, db: Session, categories: List[str]) -> SystemSettings:
        """Set list of KPI categories."""
        setting = self.get(db, key="kpi_categories")
        categories_json = json.dumps(categories)

        if setting:
            setting.value = categories_json
            db.add(setting)
        else:
            setting = SystemSettings(
                key="kpi_categories",
                value=categories_json,
                description="Available KPI categories"
            )
            db.add(setting)

        db.commit()
        db.refresh(setting)
        return setting

    def add_category(self, db: Session, category: str) -> List[str]:
        """Add a new category."""
        categories = self.get_categories(db)
        if category not in categories:
            categories.append(category)
            self.set_categories(db, categories)
        return categories

    def remove_category(self, db: Session, category: str) -> List[str]:
        """Remove a category."""
        categories = self.get_categories(db)
        if category in categories:
            categories.remove(category)
            self.set_categories(db, categories)
        return categories


system_settings = CRUDSystemSettings()
