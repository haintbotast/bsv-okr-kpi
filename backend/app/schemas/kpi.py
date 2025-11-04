"""KPI related schemas."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


# ============================================================================
# KPI Template Schemas
# ============================================================================

class KPITemplateBase(BaseModel):
    """Base KPI template schema."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)
    role: Optional[str] = Field(None, max_length=20)
    measurement_method: Optional[str] = Field(None, max_length=50)
    target_type: Optional[str] = Field(None, max_length=50)


class KPITemplateCreate(KPITemplateBase):
    """Schema for creating a KPI template."""
    pass


class KPITemplateUpdate(BaseModel):
    """Schema for updating a KPI template."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)
    role: Optional[str] = Field(None, max_length=20)
    measurement_method: Optional[str] = Field(None, max_length=50)
    target_type: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class KPITemplateResponse(KPITemplateBase):
    """Schema for KPI template response."""
    id: int
    created_by: Optional[int]
    created_at: datetime
    is_active: bool

    model_config = {"from_attributes": True}


# ============================================================================
# KPI Schemas
# ============================================================================

class KPIBase(BaseModel):
    """Base KPI schema."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    year: int = Field(..., ge=2000, le=2100)
    quarter: str = Field(..., pattern="^Q[1-4]$")
    category: Optional[str] = Field(None, max_length=50)
    target_value: Optional[str] = Field(None, max_length=100)
    current_value: Optional[str] = Field(None, max_length=100)
    progress_percentage: Optional[float] = Field(None, ge=0, le=100)
    measurement_method: Optional[str] = Field(None, max_length=50)
    template_id: Optional[int] = None

    @field_validator('quarter')
    @classmethod
    def validate_quarter(cls, v: str) -> str:
        """Validate quarter format."""
        if v not in ['Q1', 'Q2', 'Q3', 'Q4']:
            raise ValueError('Quarter must be Q1, Q2, Q3, or Q4')
        return v


class KPICreate(KPIBase):
    """Schema for creating a KPI."""
    pass


class KPIUpdate(BaseModel):
    """Schema for updating a KPI."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)
    target_value: Optional[str] = Field(None, max_length=100)
    current_value: Optional[str] = Field(None, max_length=100)
    progress_percentage: Optional[float] = Field(None, ge=0, le=100)
    measurement_method: Optional[str] = Field(None, max_length=50)


class KPIResponse(KPIBase):
    """Schema for KPI response."""
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    submitted_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None
    approved_by: Optional[int] = None

    model_config = {"from_attributes": True}


class KPIListResponse(BaseModel):
    """Schema for KPI list response with pagination."""
    items: List[KPIResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============================================================================
# KPI Evidence Schemas
# ============================================================================

class KPIEvidenceBase(BaseModel):
    """Base KPI evidence schema."""
    file_name: str = Field(..., max_length=255)
    description: Optional[str] = None


class KPIEvidenceCreate(KPIEvidenceBase):
    """Schema for creating KPI evidence."""
    file_path: str = Field(..., max_length=500)
    file_type: Optional[str] = Field(None, max_length=100)
    file_size: Optional[int] = None


class KPIEvidenceResponse(KPIEvidenceBase):
    """Schema for KPI evidence response."""
    id: int
    kpi_id: int
    file_path: str
    file_type: Optional[str]
    file_size: Optional[int]
    uploaded_by: int
    uploaded_at: datetime

    model_config = {"from_attributes": True}


# ============================================================================
# KPI Comment Schemas
# ============================================================================

class KPICommentBase(BaseModel):
    """Base KPI comment schema."""
    comment: str = Field(..., min_length=1)


class KPICommentCreate(KPICommentBase):
    """Schema for creating a KPI comment."""
    pass


class KPICommentResponse(KPICommentBase):
    """Schema for KPI comment response."""
    id: int
    kpi_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ============================================================================
# KPI History Schemas
# ============================================================================

class KPIHistoryResponse(BaseModel):
    """Schema for KPI history response."""
    id: int
    kpi_id: int
    user_id: int
    action: str
    old_value: Optional[str]
    new_value: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# ============================================================================
# KPI Statistics Schemas
# ============================================================================

class KPIStatistics(BaseModel):
    """Schema for KPI statistics."""
    total_kpis: int = 0
    draft: int = 0
    submitted: int = 0
    approved: int = 0
    rejected: int = 0
    average_progress: float = 0.0
    completion_rate: float = 0.0


class DashboardStatistics(BaseModel):
    """Schema for dashboard statistics."""
    total_kpis: int = 0
    pending_approval: int = 0
    approved: int = 0
    rejected: int = 0
    my_kpis: int = 0
    average_progress: float = 0.0
    quarterly_stats: List[dict] = []


# ============================================================================
# KPI Action Schemas
# ============================================================================

class KPISubmit(BaseModel):
    """Schema for submitting a KPI for approval."""
    pass


class KPIApprove(BaseModel):
    """Schema for approving a KPI."""
    comment: Optional[str] = None


class KPIReject(BaseModel):
    """Schema for rejecting a KPI."""
    reason: str = Field(..., min_length=1)
