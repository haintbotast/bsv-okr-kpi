"""Notification schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NotificationBase(BaseModel):
    """Base notification schema."""
    title: str = Field(..., max_length=255)
    message: str
    type: Optional[str] = Field("info", max_length=20)
    link: Optional[str] = Field(None, max_length=500)


class NotificationCreate(NotificationBase):
    """Schema for creating a notification."""
    pass


class NotificationResponse(NotificationBase):
    """Schema for notification response."""
    id: int
    user_id: int
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationUpdate(BaseModel):
    """Schema for updating a notification."""
    is_read: Optional[bool] = None


class UnreadCount(BaseModel):
    """Schema for unread notification count."""
    count: int
