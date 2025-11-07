"""Pydantic schemas for objectives."""

from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict


# ObjectiveKPILink schemas
class ObjectiveKPILinkBase(BaseModel):
    """Base schema for objective-KPI link."""
    kpi_id: int
    weight: float = Field(default=1.0, ge=0.0, le=1.0, description="Weight of KPI contribution (0-1)")


class ObjectiveKPILinkCreate(ObjectiveKPILinkBase):
    """Schema for creating objective-KPI link."""
    pass


class ObjectiveKPILinkResponse(ObjectiveKPILinkBase):
    """Schema for objective-KPI link response."""
    id: int
    objective_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Objective schemas
class ObjectiveBase(BaseModel):
    """Base schema for objective."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    level: str = Field(..., pattern="^(company|unit|division|team|individual)$")
    parent_id: Optional[int] = None
    department: Optional[str] = Field(None, max_length=100)
    year: int = Field(..., ge=2020, le=2100)
    quarter: Optional[str] = Field(None, pattern="^(Q1|Q2|Q3|Q4)$")
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = Field(default="active", pattern="^(active|completed|abandoned|on_hold)$")


class ObjectiveCreate(ObjectiveBase):
    """Schema for creating objective."""
    owner_id: int


class ObjectiveUpdate(BaseModel):
    """Schema for updating objective."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    level: Optional[str] = Field(None, pattern="^(company|unit|division|team|individual)$")
    parent_id: Optional[int] = None
    department: Optional[str] = Field(None, max_length=100)
    year: Optional[int] = Field(None, ge=2020, le=2100)
    quarter: Optional[str] = Field(None, pattern="^(Q1|Q2|Q3|Q4)$")
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = Field(None, pattern="^(active|completed|abandoned|on_hold)$")
    progress_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    owner_id: Optional[int] = None


class ObjectiveResponse(ObjectiveBase):
    """Schema for objective response."""
    id: int
    owner_id: int
    progress_percentage: float
    created_at: datetime
    updated_at: datetime
    created_by: int

    model_config = ConfigDict(from_attributes=True)


class ObjectiveDetail(ObjectiveResponse):
    """Schema for detailed objective response with relationships."""
    owner_name: Optional[str] = None
    parent_title: Optional[str] = None
    children_count: int = 0
    kpi_count: int = 0


class ObjectiveListResponse(BaseModel):
    """Schema for objective list response with pagination."""
    items: List["ObjectiveDetail"]
    total: int
    page: int
    page_size: int
    total_pages: int


class ObjectiveTreeNode(BaseModel):
    """Schema for objective tree node (recursive structure)."""
    id: int
    title: str
    level: str
    progress_percentage: float
    status: str
    owner_id: int
    owner_name: Optional[str] = None
    children: List["ObjectiveTreeNode"] = []

    model_config = ConfigDict(from_attributes=True)


class ObjectiveGanttItem(BaseModel):
    """Schema for Gantt chart item."""
    id: int
    title: str
    level: str
    start_date: Optional[date]
    end_date: Optional[date]
    progress_percentage: float
    status: str
    parent_id: Optional[int]
    dependencies: List[int] = []  # IDs of objectives this depends on

    model_config = ConfigDict(from_attributes=True)


class ObjectiveStats(BaseModel):
    """Schema for objective statistics."""
    total: int = 0
    by_level: dict = Field(default_factory=dict)
    by_status: dict = Field(default_factory=dict)
    average_progress: float = 0.0


class ProgressCalculation(BaseModel):
    """Schema for progress calculation result."""
    objective_id: int
    progress_percentage: float
    calculation_method: str  # 'children', 'kpis', 'manual'
    child_count: int = 0
    kpi_count: int = 0
    last_calculated: datetime
