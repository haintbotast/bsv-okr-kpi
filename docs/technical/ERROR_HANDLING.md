# Error Handling Guide - KPI Management System

**Purpose**: Standardize error handling across backend and frontend for consistent user experience and easier debugging.

---

## Table of Contents

1. [Backend Error Handling](#backend-error-handling)
2. [Frontend Error Handling](#frontend-error-handling)
3. [Error Response Format](#error-response-format)
4. [Error Codes](#error-codes)
5. [Logging Strategy](#logging-strategy)
6. [Best Practices](#best-practices)

---

## Backend Error Handling

### Standard Error Response Format

All API errors should return a consistent JSON structure:

```json
{
  "error": "Short error title",
  "detail": "Detailed error message for developers",
  "code": "ERROR_CODE",
  "field": "field_name",  // Optional: for validation errors
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Exception Hierarchy

```python
# app/exceptions.py

class BaseAPIException(Exception):
    """Base exception for all API errors."""
    def __init__(self, message: str, code: str = None, status_code: int = 400):
        self.message = message
        self.code = code or "API_ERROR"
        self.status_code = status_code
        super().__init__(self.message)

class ValidationError(BaseAPIException):
    """Raised when request validation fails."""
    def __init__(self, message: str, field: str = None):
        super().__init__(message, "VALIDATION_ERROR", 400)
        self.field = field

class AuthenticationError(BaseAPIException):
    """Raised when authentication fails."""
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, "AUTHENTICATION_ERROR", 401)

class AuthorizationError(BaseAPIException):
    """Raised when user lacks permission."""
    def __init__(self, message: str = "Permission denied"):
        super().__init__(message, "AUTHORIZATION_ERROR", 403)

class NotFoundError(BaseAPIException):
    """Raised when resource not found."""
    def __init__(self, resource: str, id: int = None):
        message = f"{resource} not found"
        if id:
            message = f"{resource} with id {id} not found"
        super().__init__(message, "NOT_FOUND", 404)

class ConflictError(BaseAPIException):
    """Raised when resource already exists."""
    def __init__(self, message: str):
        super().__init__(message, "CONFLICT", 409)

class RateLimitError(BaseAPIException):
    """Raised when rate limit exceeded."""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, "RATE_LIMIT_EXCEEDED", 429)

class InternalServerError(BaseAPIException):
    """Raised for unexpected server errors."""
    def __init__(self, message: str = "Internal server error"):
        super().__init__(message, "INTERNAL_ERROR", 500)
```

### Global Exception Handler

```python
# app/main.py

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.exceptions import BaseAPIException
import logging
from datetime import datetime

app = FastAPI()
logger = logging.getLogger(__name__)

@app.exception_handler(BaseAPIException)
async def api_exception_handler(request: Request, exc: BaseAPIException):
    """Handle custom API exceptions."""
    logger.error(f"{exc.code}: {exc.message}", exc_info=True)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "code": exc.code,
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url),
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    logger.warning(f"Validation error: {errors}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation failed",
            "code": "VALIDATION_ERROR",
            "details": errors,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)

    # Don't expose internal error details in production
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "code": "INTERNAL_ERROR",
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
```

### Usage in Endpoints

```python
# app/api/v1/kpis.py

from fastapi import APIRouter, Depends, HTTPException
from app.exceptions import NotFoundError, AuthorizationError
from app.crud import kpi as crud_kpi
from app.models import User

router = APIRouter()

@router.get("/kpis/{kpi_id}")
async def get_kpi(
    kpi_id: int,
    current_user: User = Depends(get_current_user)
):
    # Get KPI from database
    kpi = crud_kpi.get(kpi_id)

    # Check if exists
    if not kpi:
        raise NotFoundError("KPI", kpi_id)

    # Check permissions
    if kpi.user_id != current_user.id and current_user.role not in ["admin", "manager"]:
        raise AuthorizationError("You don't have permission to view this KPI")

    return kpi

@router.post("/kpis")
async def create_kpi(
    kpi_data: KPICreate,
    current_user: User = Depends(get_current_user)
):
    try:
        kpi = crud_kpi.create(kpi_data, user_id=current_user.id)
        return kpi
    except IntegrityError as e:
        # Handle database constraint violations
        raise ConflictError(f"KPI with this title already exists for {kpi_data.quarter}")
    except Exception as e:
        logger.error(f"Failed to create KPI: {str(e)}", exc_info=True)
        raise InternalServerError("Failed to create KPI")
```

### Database Error Handling

```python
# app/crud/base.py

from sqlalchemy.exc import IntegrityError, OperationalError
from app.exceptions import ConflictError, InternalServerError
import logging

logger = logging.getLogger(__name__)

class CRUDBase:
    def __init__(self, model):
        self.model = model

    def create(self, db, obj_in):
        try:
            obj = self.model(**obj_in.dict())
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity error: {str(e)}")
            raise ConflictError("Resource already exists or constraint violation")
        except OperationalError as e:
            db.rollback()
            logger.error(f"Database error: {str(e)}")
            raise InternalServerError("Database operation failed")
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error in create: {str(e)}", exc_info=True)
            raise InternalServerError("Failed to create resource")
```

---

## Frontend Error Handling

### API Error Handling with Axios

```js
// services/api.js - Enhanced error handling

import axios from 'axios'
import { toast } from 'react-toastify'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
})

// Response interceptor - handle errors
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    // Network error
    if (!error.response) {
      toast.error('Network error. Please check your connection.')
      return Promise.reject({
        code: 'NETWORK_ERROR',
        message: 'Network error',
      })
    }

    const { status, data } = error.response

    // Handle specific status codes
    switch (status) {
      case 400:
        // Bad request - show validation errors
        if (data.details) {
          // Multiple validation errors
          data.details.forEach(err => {
            toast.error(`${err.field}: ${err.message}`)
          })
        } else {
          toast.error(data.error || 'Invalid request')
        }
        break

      case 401:
        // Unauthorized - try token refresh
        if (!originalRequest._retry) {
          originalRequest._retry = true
          try {
            const refreshToken = localStorage.getItem('refresh_token')
            const response = await axios.post(`${api.defaults.baseURL}/auth/refresh`, {
              refresh_token: refreshToken,
            })
            localStorage.setItem('access_token', response.data.access_token)
            originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`
            return api(originalRequest)
          } catch (refreshError) {
            // Refresh failed - logout
            localStorage.clear()
            window.location.href = '/login'
            toast.error('Session expired. Please login again.')
            return Promise.reject(refreshError)
          }
        }
        break

      case 403:
        // Forbidden
        toast.error('You do not have permission to perform this action')
        break

      case 404:
        // Not found
        toast.error(data.error || 'Resource not found')
        break

      case 409:
        // Conflict
        toast.error(data.error || 'Resource already exists')
        break

      case 422:
        // Validation error
        toast.error(data.error || 'Validation failed')
        break

      case 429:
        // Rate limit
        toast.error('Too many requests. Please try again later.')
        break

      case 500:
      case 502:
      case 503:
        // Server errors
        toast.error('Server error. Please try again later.')
        break

      default:
        toast.error('An unexpected error occurred')
    }

    return Promise.reject(error.response.data)
  }
)

export default api
```

### Service Layer Error Handling

```js
// services/kpiService.js

import api from './api'

export const kpiService = {
  getAll: async (filters = {}) => {
    try {
      const response = await api.get('/kpis', { params: filters })
      return {
        success: true,
        data: response.data,
      }
    } catch (error) {
      return {
        success: false,
        error: error.code || 'UNKNOWN_ERROR',
        message: error.error || 'Failed to fetch KPIs',
      }
    }
  },

  create: async data => {
    try {
      const response = await api.post('/kpis', data)
      return {
        success: true,
        data: response.data,
      }
    } catch (error) {
      return {
        success: false,
        error: error.code || 'UNKNOWN_ERROR',
        message: error.error || 'Failed to create KPI',
        details: error.details,
      }
    }
  },
}
```

### React Component Error Handling

```jsx
// components/kpi/KPIList.jsx

import { useState, useEffect } from 'react'
import { kpiService } from '@services/kpiService'
import { useNotification } from '@hooks/useNotification'

function KPIList() {
  const [kpis, setKpis] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const { showToast } = useNotification()

  useEffect(() => {
    loadKPIs()
  }, [])

  const loadKPIs = async () => {
    try {
      setLoading(true)
      setError(null)

      const result = await kpiService.getAll()

      if (result.success) {
        setKpis(result.data.items)
      } else {
        setError(result.message)
        showToast(result.message, 'error')
      }
    } catch (error) {
      setError('An unexpected error occurred')
      showToast('Failed to load KPIs', 'error')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div>Loading...</div>
  if (error) return <div className="error-message">{error}</div>

  return (
    <div>
      {kpis.map(kpi => (
        <KPICard key={kpi.id} kpi={kpi} />
      ))}
    </div>
  )
}
```

### Error Boundary Component

```jsx
// components/common/ErrorBoundary.jsx

import { Component } from 'react'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    // Log to error reporting service
    console.error('Error caught by boundary:', error, errorInfo)

    // Send to Sentry or similar service
    // Sentry.captureException(error, { extra: errorInfo })
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-container">
          <h1>Something went wrong</h1>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()}>
            Reload Page
          </button>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
```

---

## Error Codes

### Authentication & Authorization (1xxx)
- `1001` - `AUTHENTICATION_ERROR` - Invalid credentials
- `1002` - `TOKEN_EXPIRED` - Access token expired
- `1003` - `TOKEN_INVALID` - Malformed or invalid token
- `1004` - `AUTHORIZATION_ERROR` - Insufficient permissions
- `1005` - `ACCOUNT_DISABLED` - User account is inactive

### Validation (2xxx)
- `2001` - `VALIDATION_ERROR` - Request validation failed
- `2002` - `REQUIRED_FIELD` - Required field missing
- `2003` - `INVALID_FORMAT` - Invalid field format
- `2004` - `VALUE_OUT_OF_RANGE` - Value outside allowed range

### Resource (3xxx)
- `3001` - `NOT_FOUND` - Resource not found
- `3002` - `CONFLICT` - Resource already exists
- `3003` - `DUPLICATE_ENTRY` - Duplicate unique field

### File Operations (4xxx)
- `4001` - `FILE_TOO_LARGE` - File exceeds size limit
- `4002` - `INVALID_FILE_TYPE` - File type not allowed
- `4003` - `UPLOAD_FAILED` - File upload failed
- `4004` - `FILE_NOT_FOUND` - File not found

### Business Logic (5xxx)
- `5001` - `INVALID_STATUS_TRANSITION` - Cannot change status
- `5002` - `OPERATION_NOT_ALLOWED` - Operation not permitted in current state
- `5003` - `QUOTA_EXCEEDED` - User quota exceeded

### System (9xxx)
- `9001` - `INTERNAL_ERROR` - Unexpected server error
- `9002` - `DATABASE_ERROR` - Database operation failed
- `9003` - `SERVICE_UNAVAILABLE` - External service unavailable
- `9004` - `NETWORK_ERROR` - Network communication failed
- `9005` - `RATE_LIMIT_EXCEEDED` - Too many requests

---

## Logging Strategy

### Backend Logging Levels

```python
# app/config.py

import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Configure application logging."""

    # Create logger
    logger = logging.getLogger("kpi_system")
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        "/data/logs/app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Usage in application
logger = setup_logging()

# Log levels:
# DEBUG - Detailed information for debugging
# INFO - General information about application flow
# WARNING - Warning messages for potentially harmful situations
# ERROR - Error messages for error events
# CRITICAL - Critical messages for severe error events
```

### What to Log

**✅ DO Log:**
- Authentication attempts (success/failure)
- Authorization failures
- Database errors
- External API errors
- File operations
- Critical business logic operations
- Performance metrics
- Exception stack traces (in development)

**❌ DON'T Log:**
- Passwords or tokens
- Personal identifiable information (PII)
- Credit card numbers
- Full request/response bodies (unless debugging)

### Example Logging

```python
logger.info(f"User {user.id} logged in successfully")
logger.warning(f"Failed login attempt for email: {email}")
logger.error(f"Failed to create KPI: {str(e)}", exc_info=True)
logger.critical(f"Database connection lost")
```

---

## Best Practices

### Backend

1. **Use custom exceptions** for different error types
2. **Never expose sensitive data** in error messages
3. **Log all errors** with context
4. **Provide actionable error messages** to users
5. **Handle database errors gracefully**
6. **Validate input early** (Pydantic schemas)
7. **Use HTTP status codes correctly**

### Frontend

1. **Always handle promise rejections**
2. **Show user-friendly error messages**
3. **Use error boundaries** for React errors
4. **Retry failed requests** when appropriate
5. **Log errors to monitoring service** (Sentry, etc.)
6. **Display loading and error states**
7. **Provide retry mechanisms** for users

### Error Messages

**❌ Bad:**
- "Error 500"
- "Something went wrong"
- "NoneType object has no attribute 'id'"

**✅ Good:**
- "Failed to save KPI. Please check your internet connection and try again."
- "This KPI title already exists for Q1 2024. Please choose a different title."
- "You don't have permission to approve KPIs. Contact your manager."

---

## Testing Error Scenarios

### Backend Tests

```python
# tests/test_kpi.py

def test_create_kpi_unauthorized(client):
    """Test creating KPI without authentication."""
    response = client.post("/api/v1/kpis", json={
        "title": "Test KPI",
        "category": "goal"
    })
    assert response.status_code == 401
    assert response.json()["code"] == "AUTHENTICATION_ERROR"

def test_get_kpi_not_found(client, auth_headers):
    """Test getting non-existent KPI."""
    response = client.get("/api/v1/kpis/99999", headers=auth_headers)
    assert response.status_code == 404
    assert "not found" in response.json()["error"].lower()

def test_create_kpi_validation_error(client, auth_headers):
    """Test creating KPI with invalid data."""
    response = client.post("/api/v1/kpis",
        json={"title": "A"},  # Too short
        headers=auth_headers
    )
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"
```

### Frontend Tests

```jsx
// tests/KPIList.test.jsx

import { render, screen, waitFor } from '@testing-library/react'
import KPIList from '@components/kpi/KPIList'
import { kpiService } from '@services/kpiService'

jest.mock('@services/kpiService')

test('displays error message when fetch fails', async () => {
  kpiService.getAll.mockResolvedValue({
    success: false,
    message: 'Failed to load KPIs',
  })

  render(<KPIList />)

  await waitFor(() => {
    expect(screen.getByText('Failed to load KPIs')).toBeInTheDocument()
  })
})
```

---

**Summary**: Consistent error handling across backend and frontend ensures better user experience, easier debugging, and more maintainable code.
