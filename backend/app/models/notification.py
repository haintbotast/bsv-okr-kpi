"""Notification model."""

from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Notification(Base):
    """User notification model."""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    message = Column(Text, nullable=True)
    type = Column(String(20), nullable=True)  # info, warning, success, error
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    link = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.title}>"
