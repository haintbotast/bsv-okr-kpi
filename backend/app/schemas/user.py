"""User schemas."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    avatar_url: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.EMPLOYEE


class UserUpdate(BaseModel):
    """Schema for updating user."""
    full_name: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    avatar_url: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


class NotificationPreferences(BaseModel):
    """Schema for notification preferences."""
    email_notifications: bool = True
    notify_kpi_submitted: bool = True
    notify_kpi_approved: bool = True
    notify_kpi_rejected: bool = True
    notify_comment_mention: bool = True
    weekly_digest: bool = True


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    role: UserRole
    is_active: bool
    email_notifications: bool
    notify_kpi_submitted: bool
    notify_kpi_approved: bool
    notify_kpi_rejected: bool
    notify_comment_mention: bool
    weekly_digest: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
