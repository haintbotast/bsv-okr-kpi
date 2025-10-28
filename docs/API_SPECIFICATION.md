# API Specification - KPI Management System

**Version**: 1.0.0
**Base URL**: `http://localhost:8000/api/v1`
**Authentication**: JWT Bearer Token

---

## Table of Contents

1. [Authentication](#authentication)
2. [Users](#users)
3. [KPI Templates](#kpi-templates)
4. [KPIs](#kpis)
5. [Files/Evidence](#filesevidenc)
6. [Comments](#comments)
7. [Notifications](#notifications)
8. [Reports](#reports)
9. [Admin](#admin)
10. [System](#system)

---

## Authentication

### POST /auth/login

Login with email and password.

**Request Body:**
```json
{
  "email": "user@company.com",
  "password": "SecurePassword123!"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 28800,
  "user": {
    "id": 1,
    "email": "user@company.com",
    "username": "user",
    "full_name": "John Doe",
    "role": "employee",
    "department": "IT",
    "position": "Developer"
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Account is inactive

---

### POST /auth/refresh

Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 28800
}
```

---

### POST /auth/logout

Logout current user (invalidate tokens).

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "message": "Successfully logged out"
}
```

---

### POST /auth/forgot-password

Request password reset email.

**Request Body:**
```json
{
  "email": "user@company.com"
}
```

**Response:** `200 OK`
```json
{
  "message": "Password reset email sent"
}
```

---

### POST /auth/reset-password

Reset password with token.

**Request Body:**
```json
{
  "token": "reset_token_here",
  "new_password": "NewPassword123!"
}
```

**Response:** `200 OK`
```json
{
  "message": "Password successfully reset"
}
```

---

## Users

### GET /users/me

Get current user profile.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@company.com",
  "username": "user",
  "full_name": "John Doe",
  "role": "employee",
  "department": "IT",
  "position": "Developer",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

---

### PUT /users/me

Update current user profile.

**Request Body:**
```json
{
  "full_name": "John Doe Updated",
  "position": "Senior Developer"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@company.com",
  "full_name": "John Doe Updated",
  "position": "Senior Developer"
}
```

---

### PUT /users/me/password

Change current user password.

**Request Body:**
```json
{
  "current_password": "OldPassword123!",
  "new_password": "NewPassword123!"
}
```

**Response:** `200 OK`
```json
{
  "message": "Password successfully changed"
}
```

---

### GET /users

List all users (Admin/Manager only).

**Query Parameters:**
- `page` (integer, default: 1)
- `page_size` (integer, default: 20, max: 100)
- `role` (string, optional): Filter by role
- `department` (string, optional): Filter by department
- `is_active` (boolean, optional): Filter by active status
- `search` (string, optional): Search by name or email

**Response:** `200 OK`
```json
{
  "total": 30,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": 1,
      "email": "user@company.com",
      "username": "user",
      "full_name": "John Doe",
      "role": "employee",
      "department": "IT",
      "position": "Developer",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

### GET /users/{user_id}

Get specific user details (Admin/Manager only).

**Response:** `200 OK`
```json
{
  "id": 1,
  "email": "user@company.com",
  "username": "user",
  "full_name": "John Doe",
  "role": "employee",
  "department": "IT",
  "position": "Developer",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

---

### POST /users (Admin only)

Create new user.

**Request Body:**
```json
{
  "email": "newuser@company.com",
  "username": "newuser",
  "password": "SecurePassword123!",
  "full_name": "Jane Smith",
  "role": "employee",
  "department": "HR",
  "position": "HR Manager"
}
```

**Response:** `201 Created`
```json
{
  "id": 2,
  "email": "newuser@company.com",
  "username": "newuser",
  "full_name": "Jane Smith",
  "role": "employee",
  "department": "HR",
  "position": "HR Manager",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

### PUT /users/{user_id} (Admin only)

Update user.

**Request Body:**
```json
{
  "full_name": "Jane Smith Updated",
  "role": "manager",
  "is_active": true
}
```

**Response:** `200 OK`

---

### DELETE /users/{user_id} (Admin only)

Deactivate user (soft delete).

**Response:** `200 OK`
```json
{
  "message": "User successfully deactivated"
}
```

---

## KPI Templates

### GET /templates

List all KPI templates.

**Query Parameters:**
- `page`, `page_size`
- `category` (string): Filter by category
- `role` (string): Filter by target role
- `is_active` (boolean)

**Response:** `200 OK`
```json
{
  "total": 10,
  "items": [
    {
      "id": 1,
      "name": "Website Uptime",
      "description": "Maintain website uptime above 99.5%",
      "category": "goal",
      "role": "employee",
      "measurement_method": "Monitoring tools",
      "target_type": "percentage",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

### GET /templates/{template_id}

Get specific template.

**Response:** `200 OK`

---

### POST /templates (Admin only)

Create new template.

**Request Body:**
```json
{
  "name": "Code Review Quality",
  "description": "Maintain code review approval rate above 90%",
  "category": "goal",
  "role": "employee",
  "measurement_method": "GitLab/GitHub statistics",
  "target_type": "percentage"
}
```

**Response:** `201 Created`

---

### PUT /templates/{template_id} (Admin only)

Update template.

---

### DELETE /templates/{template_id} (Admin only)

Delete template (soft delete).

---

## KPIs

### GET /kpis

List KPIs (filtered by user role).

**Query Parameters:**
- `page`, `page_size`
- `user_id` (integer): Filter by user
- `year` (integer): Filter by year
- `quarter` (string): Filter by quarter (Q1, Q2, Q3, Q4)
- `status` (string): Filter by status (draft, submitted, approved, rejected)
- `category` (string): Filter by category
- `search` (string): Search in title/description

**Response:** `200 OK`
```json
{
  "total": 50,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": 1,
      "user_id": 1,
      "user_name": "John Doe",
      "template_id": 1,
      "year": 2024,
      "quarter": "Q1",
      "title": "Improve website uptime",
      "description": "Maintain 99.9% uptime for company website",
      "category": "goal",
      "target_value": "99.9",
      "current_value": "99.7",
      "progress_percentage": 97.8,
      "measurement_method": "UptimeRobot monitoring",
      "status": "approved",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-15T00:00:00Z",
      "submitted_at": "2024-01-10T00:00:00Z",
      "approved_at": "2024-01-15T00:00:00Z",
      "approved_by": 2,
      "approved_by_name": "Manager Name"
    }
  ]
}
```

---

### GET /kpis/{kpi_id}

Get specific KPI details.

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "user": {
    "id": 1,
    "full_name": "John Doe",
    "department": "IT"
  },
  "template_id": 1,
  "template": {
    "id": 1,
    "name": "Website Uptime"
  },
  "year": 2024,
  "quarter": "Q1",
  "title": "Improve website uptime",
  "description": "Maintain 99.9% uptime for company website",
  "category": "goal",
  "target_value": "99.9",
  "current_value": "99.7",
  "progress_percentage": 97.8,
  "measurement_method": "UptimeRobot monitoring",
  "status": "approved",
  "evidence_count": 3,
  "comment_count": 5,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T00:00:00Z",
  "submitted_at": "2024-01-10T00:00:00Z",
  "approved_at": "2024-01-15T00:00:00Z",
  "approved_by": 2,
  "approved_by_name": "Manager Name"
}
```

---

### POST /kpis

Create new KPI.

**Request Body:**
```json
{
  "template_id": 1,
  "year": 2024,
  "quarter": "Q1",
  "title": "Improve website uptime",
  "description": "Maintain 99.9% uptime for company website",
  "category": "goal",
  "target_value": "99.9",
  "measurement_method": "UptimeRobot monitoring"
}
```

**Response:** `201 Created`

---

### PUT /kpis/{kpi_id}

Update KPI (owner only, or Admin).

**Request Body:**
```json
{
  "current_value": "99.8",
  "description": "Updated description"
}
```

**Response:** `200 OK`

---

### DELETE /kpis/{kpi_id}

Delete KPI (owner only, must be draft status).

**Response:** `200 OK`

---

### POST /kpis/{kpi_id}/submit

Submit KPI for approval.

**Response:** `200 OK`
```json
{
  "id": 1,
  "status": "submitted",
  "submitted_at": "2024-01-10T00:00:00Z"
}
```

---

### POST /kpis/{kpi_id}/approve (Manager/Admin only)

Approve KPI.

**Request Body:**
```json
{
  "comment": "Good progress, approved!"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "status": "approved",
  "approved_at": "2024-01-15T00:00:00Z",
  "approved_by": 2
}
```

---

### POST /kpis/{kpi_id}/reject (Manager/Admin only)

Reject KPI.

**Request Body:**
```json
{
  "reason": "Target value needs to be more specific"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "status": "rejected"
}
```

---

### GET /kpis/{kpi_id}/history

Get KPI history/audit trail.

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "kpi_id": 1,
      "user_id": 1,
      "user_name": "John Doe",
      "action": "created",
      "old_value": null,
      "new_value": "{\"title\": \"Improve website uptime\"}",
      "created_at": "2024-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "action": "updated",
      "old_value": "{\"current_value\": \"99.5\"}",
      "new_value": "{\"current_value\": \"99.7\"}",
      "created_at": "2024-01-10T00:00:00Z"
    }
  ]
}
```

---

## Files/Evidence

### GET /kpis/{kpi_id}/evidence

List evidence files for a KPI.

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "kpi_id": 1,
      "file_name": "uptime_report_january.pdf",
      "file_path": "/uploads/evidence/uuid-filename.pdf",
      "file_type": "application/pdf",
      "file_size": 1048576,
      "uploaded_by": 1,
      "uploaded_by_name": "John Doe",
      "uploaded_at": "2024-01-15T00:00:00Z",
      "description": "Monthly uptime report"
    }
  ]
}
```

---

### POST /kpis/{kpi_id}/evidence

Upload evidence file.

**Request:**
- Content-Type: `multipart/form-data`
- Fields:
  - `file`: File binary
  - `description`: Optional description

**Response:** `201 Created`
```json
{
  "id": 1,
  "file_name": "uptime_report.pdf",
  "file_size": 1048576,
  "file_type": "application/pdf",
  "uploaded_at": "2024-01-15T00:00:00Z"
}
```

**Error Responses:**
- `400 Bad Request`: File too large or invalid type
- `413 Payload Too Large`: File exceeds 50MB limit

---

### GET /files/{file_id}

Download evidence file.

**Response:** `200 OK`
- Content-Type: Based on file type
- Content-Disposition: attachment; filename="filename.pdf"

---

### DELETE /files/{file_id}

Delete evidence file (owner or Admin only).

**Response:** `200 OK`

---

## Comments

### GET /kpis/{kpi_id}/comments

List comments for a KPI.

**Response:** `200 OK`
```json
{
  "items": [
    {
      "id": 1,
      "kpi_id": 1,
      "user_id": 2,
      "user_name": "Manager Name",
      "comment": "Great progress! Keep it up.",
      "created_at": "2024-01-15T00:00:00Z",
      "updated_at": "2024-01-15T00:00:00Z"
    }
  ]
}
```

---

### POST /kpis/{kpi_id}/comments

Add comment to KPI.

**Request Body:**
```json
{
  "comment": "Updated with latest metrics"
}
```

**Response:** `201 Created`

---

### PUT /comments/{comment_id}

Update comment (owner only).

**Request Body:**
```json
{
  "comment": "Updated comment text"
}
```

**Response:** `200 OK`

---

### DELETE /comments/{comment_id}

Delete comment (owner or Admin only).

**Response:** `200 OK`

---

## Notifications

### GET /notifications

List notifications for current user.

**Query Parameters:**
- `page`, `page_size`
- `is_read` (boolean): Filter by read status
- `type` (string): Filter by notification type

**Response:** `200 OK`
```json
{
  "total": 10,
  "unread_count": 3,
  "items": [
    {
      "id": 1,
      "user_id": 1,
      "title": "KPI Approved",
      "message": "Your KPI 'Improve website uptime' has been approved",
      "type": "success",
      "is_read": false,
      "link": "/kpis/1",
      "created_at": "2024-01-15T00:00:00Z"
    }
  ]
}
```

---

### PUT /notifications/{notification_id}/read

Mark notification as read.

**Response:** `200 OK`

---

### PUT /notifications/read-all

Mark all notifications as read.

**Response:** `200 OK`

---

## Reports

### GET /reports/user/{user_id}

Generate user report (PDF/Excel).

**Query Parameters:**
- `year` (integer, required)
- `quarter` (string, optional): Q1, Q2, Q3, Q4, or "all"
- `format` (string, default: pdf): pdf or excel

**Response:** `200 OK`
- Content-Type: application/pdf or application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
- Content-Disposition: attachment; filename="user_report_2024_Q1.pdf"

---

### GET /reports/department

Generate department report (Manager/Admin only).

**Query Parameters:**
- `department` (string, required)
- `year`, `quarter`, `format`

**Response:** `200 OK`

---

### GET /reports/company (Admin only)

Generate company-wide report.

**Query Parameters:**
- `year`, `quarter`, `format`

**Response:** `200 OK`

---

### GET /analytics/dashboard

Get dashboard analytics.

**Query Parameters:**
- `year` (integer, default: current year)
- `quarter` (string, optional)

**Response:** `200 OK`
```json
{
  "summary": {
    "total_kpis": 50,
    "approved_kpis": 35,
    "pending_kpis": 10,
    "rejected_kpis": 5,
    "average_progress": 87.5
  },
  "by_quarter": {
    "Q1": {"total": 15, "approved": 12, "avg_progress": 90.5},
    "Q2": {"total": 12, "approved": 10, "avg_progress": 85.0}
  },
  "by_category": {
    "goal": {"total": 20, "approved": 18},
    "mission": {"total": 15, "approved": 10},
    "task": {"total": 15, "approved": 7}
  },
  "by_department": {
    "IT": {"total": 30, "avg_progress": 88.0},
    "HR": {"total": 10, "avg_progress": 85.0},
    "Sales": {"total": 10, "avg_progress": 90.0}
  }
}
```

---

## Admin

### GET /admin/users

List all users with admin details.

---

### GET /admin/system-settings

Get system settings.

**Response:** `200 OK`
```json
{
  "settings": [
    {
      "key": "system_name",
      "value": "KPI Management System",
      "description": "Application name"
    },
    {
      "key": "allow_registration",
      "value": "false",
      "description": "Allow public user registration"
    }
  ]
}
```

---

### PUT /admin/system-settings

Update system settings.

**Request Body:**
```json
{
  "settings": [
    {
      "key": "allow_registration",
      "value": "true"
    }
  ]
}
```

---

### GET /admin/audit-log

Get audit log.

**Query Parameters:**
- `page`, `page_size`
- `user_id`, `action`, `start_date`, `end_date`

**Response:** `200 OK`

---

### POST /admin/backup

Trigger manual backup.

**Response:** `200 OK`
```json
{
  "message": "Backup started",
  "backup_file": "backup_20240115_120000.db"
}
```

---

### GET /admin/backups

List available backups.

**Response:** `200 OK`
```json
{
  "items": [
    {
      "filename": "backup_20240115_120000.db",
      "size": 10485760,
      "created_at": "2024-01-15T12:00:00Z"
    }
  ]
}
```

---

## System

### GET /health

Health check endpoint (public).

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T12:00:00Z",
  "version": "1.0.0"
}
```

---

### GET /version

Get API version info (public).

**Response:** `200 OK`
```json
{
  "version": "1.0.0",
  "api_version": "v1",
  "environment": "production"
}
```

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-15T12:00:00Z"
}
```

### Common HTTP Status Codes:
- `200 OK`: Success
- `201 Created`: Resource created
- `204 No Content`: Success with no response body
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict
- `413 Payload Too Large`: File too large
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

---

## Authentication

All authenticated endpoints require JWT token in header:

```
Authorization: Bearer {access_token}
```

Token expires after 8 hours. Use refresh token to get new access token.

---

## Rate Limiting

(Optional, if enabled)

- Default: 60 requests per minute per user
- Exceeded requests return `429 Too Many Requests`

---

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

**Response Format:**
```json
{
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5,
  "items": [...]
}
```

---

## Filtering & Sorting

**Common query parameters:**
- `sort_by`: Field name to sort
- `order`: `asc` or `desc` (default: desc)
- `search`: Full-text search

**Example:**
```
GET /api/v1/kpis?year=2024&quarter=Q1&status=approved&sort_by=created_at&order=desc
```

---

## File Upload Requirements

**Allowed file types:**
- Documents: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX
- Images: JPG, JPEG, PNG, GIF

**File size limit:** 50 MB per file

**Content-Type:** `multipart/form-data`

---

## Webhooks (Future Enhancement)

Not implemented in v1.0.0

---

## API Versioning

Current version: **v1**

Base URL includes version: `/api/v1/`

Future versions will use: `/api/v2/`, etc.

---

## Support

For API support, contact: support@company.com

API Documentation (Swagger UI): http://localhost:8000/docs
API Documentation (ReDoc): http://localhost:8000/redoc
