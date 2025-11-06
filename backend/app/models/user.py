"""User model."""

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """User model for authentication and authorization."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(20), nullable=False, default="employee", index=True)
    department = Column(String(100), nullable=True)
    position = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Notification Preferences
    email_notifications = Column(Boolean, default=True, nullable=False)  # Master email toggle
    notify_kpi_submitted = Column(Boolean, default=True, nullable=False)  # KPI submitted for approval
    notify_kpi_approved = Column(Boolean, default=True, nullable=False)  # KPI approved
    notify_kpi_rejected = Column(Boolean, default=True, nullable=False)  # KPI rejected
    notify_comment_mention = Column(Boolean, default=True, nullable=False)  # Mentioned in comment
    weekly_digest = Column(Boolean, default=True, nullable=False)  # Weekly activity digest

    # Password Reset
    reset_token = Column(String(500), nullable=True)  # Password reset token
    reset_token_expires = Column(DateTime, nullable=True)  # Reset token expiration
    password_history = Column(Text, nullable=True)  # JSON array of last 3 password hashes

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    kpis = relationship("KPI", back_populates="user", foreign_keys="KPI.user_id")
    approved_kpis = relationship("KPI", back_populates="approver", foreign_keys="KPI.approved_by")
    templates = relationship("KPITemplate", back_populates="creator")
    comments = relationship("KPIComment", back_populates="user")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    uploaded_files = relationship("KPIEvidence", back_populates="uploader")

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
