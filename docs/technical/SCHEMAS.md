# Pydantic Schemas - KPI Management System

**Purpose**: Define all request/response models for API validation and serialization.

---

## Table of Contents

1. [Authentication Schemas](#authentication-schemas)
2. [User Schemas](#user-schemas)
3. [KPI Schemas](#kpi-schemas)
4. [KPI Template Schemas](#kpi-template-schemas)
5. [File/Evidence Schemas](#fileevidenc-schemas)
6. [Comment Schemas](#comment-schemas)
7. [Notification Schemas](#notification-schemas)
8. [Report Schemas](#report-schemas)
9. [Common/Shared Schemas](#commonshared-schemas)

---

## Authentication Schemas

### LoginRequest
```python
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@company.com",
                "password": "SecurePassword123!"
            }
        }
```

### TokenResponse
```python
from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: "UserResponse"  # Forward reference

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 28800,
                "user": {
                    "id": 1,
                    "email": "user@company.com",
                    "username": "user",
                    "full_name": "John Doe",
                    "role": "employee"
                }
            }
        }
```

### RefreshTokenRequest
```python
class RefreshTokenRequest(BaseModel):
    refresh_token: str
```

### PasswordResetRequest
```python
class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)
```

---

## User Schemas

### UserBase
```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
```

### UserCreate
```python
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.EMPLOYEE

    class Config:
        json_schema_extra = {
            "example": {
                "email": "newuser@company.com",
                "username": "newuser",
                "password": "SecurePass123!",
                "full_name": "New User",
                "role": "employee",
                "department": "IT",
                "position": "Developer"
            }
        }
```

### UserUpdate
```python
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "Updated Name",
                "position": "Senior Developer"
            }
        }
```

### UserResponse
```python
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    role: UserRole
    department: Optional[str]
    position: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### PasswordChange
```python
class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
```

---

## KPI Schemas

### KPIBase
```python
from enum import Enum
from typing import Optional

class KPICategory(str, Enum):
    MISSION = "mission"
    GOAL = "goal"
    TASK = "task"

class KPIStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"

class Quarter(str, Enum):
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"

class KPIBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    category: KPICategory
    year: int = Field(..., ge=2020, le=2100)
    quarter: Quarter
    target_value: str
    measurement_method: Optional[str] = None
```

### KPICreate
```python
class KPICreate(KPIBase):
    template_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Improve website uptime",
                "description": "Achieve 99.9% uptime for company website",
                "category": "goal",
                "year": 2024,
                "quarter": "Q1",
                "target_value": "99.9",
                "measurement_method": "percentage",
                "template_id": 1
            }
        }
```

### KPIUpdate
```python
class KPIUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    target_value: Optional[str] = None
    current_value: Optional[str] = None
    progress_percentage: Optional[float] = Field(None, ge=0, le=100)
```

### KPIResponse
```python
from datetime import datetime

class KPIResponse(KPIBase):
    id: int
    user_id: int
    template_id: Optional[int]
    current_value: Optional[str]
    progress_percentage: Optional[float]
    status: KPIStatus
    created_at: datetime
    updated_at: datetime
    submitted_at: Optional[datetime]
    approved_at: Optional[datetime]
    approved_by: Optional[int]

    # Related data
    user: Optional["UserResponse"]
    evidence_count: int = 0
    comment_count: int = 0

    class Config:
        from_attributes = True
```

### KPIStatusUpdate
```python
class KPIStatusUpdate(BaseModel):
    status: KPIStatus
    comment: Optional[str] = None
```

### KPIFilter
```python
class KPIFilter(BaseModel):
    year: Optional[int] = None
    quarter: Optional[Quarter] = None
    status: Optional[KPIStatus] = None
    category: Optional[KPICategory] = None
    user_id: Optional[int] = None
    search: Optional[str] = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
```

---

## KPI Template Schemas

### KPITemplateBase
```python
class KPITemplateBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = None
    category: KPICategory
    role: Optional[UserRole] = None
    measurement_method: Optional[str] = None
    target_type: Optional[str] = None  # percentage, number, boolean
```

### KPITemplateCreate
```python
class KPITemplateCreate(KPITemplateBase):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Server Uptime",
                "description": "Track server uptime percentage",
                "category": "goal",
                "role": "employee",
                "measurement_method": "percentage",
                "target_type": "percentage"
            }
        }
```

### KPITemplateResponse
```python
class KPITemplateResponse(KPITemplateBase):
    id: int
    created_by: Optional[int]
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
```

---

## File/Evidence Schemas

### FileUploadResponse
```python
class FileUploadResponse(BaseModel):
    id: int
    kpi_id: int
    file_name: str
    file_path: str
    file_type: str
    file_size: int
    uploaded_by: int
    uploaded_at: datetime
    description: Optional[str]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "kpi_id": 10,
                "file_name": "uptime_report.pdf",
                "file_path": "/uploads/2024/01/uuid.pdf",
                "file_type": "application/pdf",
                "file_size": 245678,
                "uploaded_by": 1,
                "uploaded_at": "2024-01-15T10:30:00Z",
                "description": "Monthly uptime report"
            }
        }
```

### FileFilter
```python
class FileFilter(BaseModel):
    kpi_id: Optional[int] = None
    uploaded_by: Optional[int] = None
    file_type: Optional[str] = None
```

---

## Comment Schemas

### CommentCreate
```python
class CommentCreate(BaseModel):
    kpi_id: int
    comment: str = Field(..., min_length=1, max_length=2000)

    class Config:
        json_schema_extra = {
            "example": {
                "kpi_id": 10,
                "comment": "Great progress on this KPI!"
            }
        }
```

### CommentUpdate
```python
class CommentUpdate(BaseModel):
    comment: str = Field(..., min_length=1, max_length=2000)
```

### CommentResponse
```python
class CommentResponse(BaseModel):
    id: int
    kpi_id: int
    user_id: int
    comment: str
    created_at: datetime
    updated_at: datetime

    # Related data
    user: Optional["UserResponse"]

    class Config:
        from_attributes = True
```

---

## Notification Schemas

### NotificationType(str, Enum):
```python
class NotificationType(str, Enum):
    INFO = "info"
    WARNING = "warning"
    SUCCESS = "success"
    ERROR = "error"
```

### NotificationCreate
```python
class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    type: NotificationType = NotificationType.INFO
    link: Optional[str] = None
```

### NotificationResponse
```python
class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: NotificationType
    is_read: bool
    link: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
```

### NotificationMarkRead
```python
class NotificationMarkRead(BaseModel):
    notification_ids: list[int]
```

---

## Report Schemas

### ReportFilter
```python
class ReportFilter(BaseModel):
    year: Optional[int] = None
    quarter: Optional[Quarter] = None
    user_id: Optional[int] = None
    department: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
```

### ReportFormat(str, Enum):
```python
class ReportFormat(str, Enum):
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
```

### ReportRequest
```python
class ReportRequest(BaseModel):
    format: ReportFormat
    filters: ReportFilter
    include_evidence: bool = False
    include_comments: bool = False
```

---

## Common/Shared Schemas

### PaginatedResponse
```python
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "page_size": 20,
                "total_pages": 5
            }
        }
```

### ErrorResponse
```python
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Validation Error",
                "detail": "Invalid email format",
                "code": "VALIDATION_ERROR"
            }
        }
```

### SuccessResponse
```python
class SuccessResponse(BaseModel):
    message: str
    data: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed successfully",
                "data": {"id": 123}
            }
        }
```

### HealthCheckResponse
```python
class HealthCheckResponse(BaseModel):
    status: str
    version: str
    database: str
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "database": "connected",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }
```

---

## Validation Rules Summary

### User Validation
- Email: Valid email format, unique
- Username: 3-50 chars, alphanumeric + underscore, unique
- Password: Minimum 8 characters
- Role: Must be one of: admin, manager, employee

### KPI Validation
- Title: 3-200 characters
- Year: 2020-2100
- Quarter: Q1, Q2, Q3, or Q4
- Progress: 0-100 (percentage)
- Status: draft → submitted → approved/rejected

### File Validation
- File types: pdf, doc, docx, xls, xlsx, ppt, pptx, jpg, jpeg, png, gif
- Max size: 50MB (52,428,800 bytes)
- Filename: Sanitized, UUID-based storage

### Comment Validation
- Comment text: 1-2000 characters

---

## Usage Example

```python
# In API endpoint
from fastapi import APIRouter, Depends
from app.schemas.kpi import KPICreate, KPIResponse

router = APIRouter()

@router.post("/kpis", response_model=KPIResponse)
async def create_kpi(
    kpi_data: KPICreate,
    current_user: User = Depends(get_current_user)
):
    # kpi_data is automatically validated
    kpi = crud.kpi.create(kpi_data, user_id=current_user.id)
    return kpi
```

---

**Next**: See [API_REFERENCE.md](./API_REFERENCE.md) for complete endpoint documentation.
