"""System settings model."""

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class SystemSettings(Base):
    """System settings key-value store."""

    __tablename__ = "system_settings"

    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<SystemSettings {self.key}={self.value}>"
