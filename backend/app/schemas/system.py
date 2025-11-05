"""System settings schemas."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SystemSettingsBase(BaseModel):
    """Base system settings schema."""
    key: str
    value: Optional[str] = None
    description: Optional[str] = None


class SystemSettingsCreate(SystemSettingsBase):
    """Schema for creating system settings."""
    pass


class SystemSettingsUpdate(BaseModel):
    """Schema for updating system settings."""
    value: Optional[str] = None
    description: Optional[str] = None


class SystemSettingsResponse(SystemSettingsBase):
    """Schema for system settings response."""
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    """Schema for creating a category."""
    name: str


class CategoryResponse(BaseModel):
    """Schema for category response."""
    name: str
