# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📌 Session Continuity

**IMPORTANT**: Always check `SESSION_NOTES.md` at the start of each session to see:
- What was recently completed
- What we're working on next
- Suggested next steps

## Project Overview

**KPI Management System** - Self-hosted, lightweight system optimized for ~30 users. Uses SQLite for simplicity and cost-effectiveness (~$154/year vs $2,500+/year for SaaS alternatives).

**Tech Stack:**
- Backend: FastAPI (Python 3.11+) + SQLAlchemy 2.0 + SQLite
- Frontend: React 18 + Vite + Tailwind CSS
- Deployment: Docker Compose (2 containers)
- Auth: JWT (8h access + 7d refresh tokens), bcrypt password hashing

**Current Status:** All Phases Complete! 🎉
- ✅ Phase 1-7: All core features (Auth, KPI, Files, Workflow, Reports, Admin, Optimization)
- ✅ Phase A: Approval workflow enhancements
- ✅ Phase B: Bug fixes & Category management
- ✅ User Profile with Avatar Upload (Nov 5, 2025)
- 🚀 Production ready - Now adding enhancements based on user needs

## Development Commands

### Backend

```bash
# Setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Database
alembic upgrade head                    # Run migrations
alembic revision --autogenerate -m ""   # Create migration
python scripts/init_db.py               # Initialize database
python scripts/create_admin.py --email admin@company.com --password Admin123! --fullname "Admin"

# Run
uvicorn app.main:app --reload           # Development server (port 8000)
uvicorn app.main:app --reload --log-level debug  # With debug logs

# Testing
pytest                                  # Run all tests
pytest tests/test_auth.py               # Run specific test file
pytest -v                               # Verbose output
pytest --cov=app tests/                 # With coverage
pytest -x                               # Stop on first failure
pytest -k "test_create"                 # Run tests matching pattern

# Code Quality
black app/                              # Format code
flake8 app/                             # Lint
isort app/                              # Sort imports
```

### Frontend

```bash
# Setup
cd frontend
npm install

# Run
npm run dev                             # Development server (port 3000)
npm run build                           # Production build
npm run preview                         # Preview production build

# Code Quality
npm run lint                            # Lint
npm run lint:fix                        # Fix lint errors
npm run format                          # Format with Prettier
```

### Docker

```bash
# Development
docker-compose up -d                    # Start all services
docker-compose logs -f backend          # View backend logs
docker-compose exec backend bash        # Shell into backend
docker-compose down                     # Stop all services

# Production
docker-compose -f deployment/docker-compose.prod.yml up -d --build
```

## Architecture & Code Patterns

### Layered Architecture (Backend)

**Critical:** Follow strict layer separation:

```
Request → API (routes) → Service (business logic) → CRUD (database ops) → Model (SQLAlchemy)
```

**Never:**
- Put business logic in API routes
- Access database directly from services (use CRUD layer)
- Return ORM models directly (use Pydantic schemas)

**Example pattern:**
```python
# ❌ Wrong: Business logic in API route
@router.post("/kpis")
def create_kpi(kpi_in: KPICreate, db: Session = Depends(get_db)):
    kpi = KPI(**kpi_in.dict())
    db.add(kpi)
    db.commit()
    return kpi

# ✅ Correct: Layered approach
@router.post("/kpis")
def create_kpi(kpi_in: KPICreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return kpi_service.create_kpi(db, kpi_in=kpi_in, current_user=user)
```

### Authentication & Authorization Pattern

**JWT Flow:**
1. Login → returns access_token (8h) + refresh_token (7d)
2. All protected endpoints require `Authorization: Bearer <access_token>`
3. Token refresh via `/api/v1/auth/refresh` endpoint

**RBAC Pattern:**
```python
# In api/deps.py - permission decorators
def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user

# Usage in routes
@router.post("/templates", dependencies=[Depends(require_admin)])
def create_template(...):
    pass
```

**Frontend auth:**
- AuthContext provides: `{ user, isAuthenticated, login, logout }`
- ProtectedRoute component wraps authenticated routes
- API interceptor auto-refreshes tokens on 401

### Database Patterns

**CRITICAL - No Deprecated Functions:**
```python
# ❌ NEVER use (deprecated in Python 3.12+)
datetime.utcnow()

# ✅ ALWAYS use
from datetime import datetime, timezone
datetime.now(timezone.utc)
```

**Pydantic v2 Syntax:**
```python
# ❌ Old (v1)
UserResponse.from_orm(user)

# ✅ New (v2)
UserResponse.model_validate(user)
```

**SQLite Optimizations:**
Already configured in `database.py`:
- WAL mode for better concurrency
- Foreign keys enabled
- Optimized cache size

### KPI State Machine

**Critical workflow states:**
```
draft → submitted → approved
                 → rejected → (can edit) → draft
```

**Business rules:**
- Only owner can edit draft/rejected KPIs
- Only managers/admins can approve/reject
- Approved KPIs cannot be edited
- All state changes logged in kpi_history

### Frontend Patterns

**Service Layer Pattern:**
```javascript
// In services/kpiService.js
export const getKPIs = async (params) => {
  const response = await api.get('/kpis', { params })
  return response.data
}

// In component
const { items } = await kpiService.getKPIs({ year: 2024 })
```

**Error Handling:**
```javascript
// Always use try-catch with toast notifications
try {
  await kpiService.createKPI(data)
  toast.success('KPI created successfully')
  navigate('/kpis')
} catch (error) {
  toast.error(error.response?.data?.detail || 'Failed to create KPI')
}
```

## Critical Implementation Notes

### DateTime Handling
**ALWAYS use timezone-aware datetime:**
```python
from datetime import datetime, timezone

# For all timestamps
created_at = datetime.now(timezone.utc)
```

### Permission Checks
**Service layer must validate permissions:**
```python
def update_kpi(self, db: Session, kpi_id: int, kpi_in: KPIUpdate, current_user: User):
    kpi = kpi_crud.get(db, kpi_id=kpi_id)

    # Check ownership
    if kpi.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Check state
    if kpi.status not in ["draft", "rejected"]:
        raise HTTPException(status_code=400, detail="Cannot edit KPI in this status")
```

### History Tracking
**All KPI changes must be logged:**
```python
def _create_history(self, db: Session, kpi_id: int, user_id: int, action: str, ...):
    history = KPIHistory(kpi_id=kpi_id, user_id=user_id, action=action, ...)
    db.add(history)
    db.commit()
```

### File Uploads (Phase 3+)
**Security requirements:**
- Validate file type (whitelist: pdf, doc, docx, xls, xlsx, jpg, png)
- Max 50MB per file
- Store with UUID filenames (never use original names)
- Save in `/data/uploads/` outside web root

## Common Pitfalls

1. **DateTime:** Never use `datetime.utcnow()` - it's deprecated
2. **Pydantic:** Use `.model_validate()` not `.from_orm()`
3. **Business Logic:** Keep it in services, not routes
4. **Permissions:** Check in service layer, not just routes
5. **State Changes:** Always log to kpi_history
6. **SQLite:** Use WAL mode (already configured)
7. **Frontend API:** Handle 401 for token refresh
8. **Error Messages:** User-friendly on frontend, detailed in logs

## Database Schema Quick Reference

**8 tables:**
1. `users` - Authentication & roles
2. `kpi_templates` - Reusable KPI templates
3. `kpis` - Main KPI records (central table)
4. `kpi_evidence` - File attachments
5. `kpi_comments` - Collaboration
6. `kpi_history` - Audit trail (auto-created)
7. `notifications` - User notifications
8. `system_settings` - Configuration

**Key relationships:**
- User → KPIs (1:N, author)
- User → KPIs (1:N, approver)
- KPI → Evidence (1:N, cascade delete)
- KPI → Comments (1:N, cascade delete)
- KPI → History (1:N, cascade delete)

## Documentation

**Vietnamese docs** (main):
- `/docs/` - Architecture, database, security, deployment

**English docs** (technical specs):
- `/docs/technical/` - API reference, development phases, schemas

**Phase completion:**
- `PHASE1_COMPLETE.md` - Auth & infrastructure
- `PHASE2_COMPLETE.md` - KPI management
- `PHASE1_AND_2_REVIEW.md` - Overall review

**Quick start:**
- `QUICKSTART.md` - 5-minute setup guide
- `CONTRIBUTING.md` - Development guidelines

## Role-Based Features

**Admin:**
- Full system access
- User management
- Template management
- System settings

**Manager:**
- Approve/reject team KPIs
- View team KPIs
- Create own KPIs
- Team reports

**Employee:**
- Create own KPIs
- Submit for approval
- Upload evidence
- Personal reports

## Testing Strategy

**Backend (pytest):**
- Unit tests for business logic
- Integration tests for API endpoints
- Target: >70% coverage
- Mock external dependencies

**Frontend:**
- Component tests (optional)
- E2E tests (Phase 7)
- Manual testing checklist in DEVELOPMENT_PHASES.md

## Performance Considerations

**SQLite limits:**
- Optimized for <100 concurrent users
- Single writer at a time (WAL mode helps)
- Not suitable for distributed systems

**Scaling path:**
- 30-100 users: Increase server resources, keep SQLite
- >100 users: Migrate to PostgreSQL, add Redis cache

**Frontend optimization:**
- Code splitting (React.lazy)
- Pagination (max 100 items)
- Image lazy loading
- Memoization (React.memo, useMemo, useCallback)

## Environment Variables

**Backend (.env):**
- `SECRET_KEY` - JWT secret (generate with `openssl rand -hex 32`)
- `DATABASE_URL` - SQLite path
- `CORS_ORIGINS` - Allowed origins (comma-separated)
- `ENVIRONMENT` - dev/staging/production

**Frontend (.env):**
- `VITE_API_URL` - Backend API URL

## Git Workflow

**Branch naming:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `refactor/` - Code refactoring

**Commit format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:** feat, fix, docs, style, refactor, test, chore

## API Documentation

**Interactive docs:** http://localhost:8000/docs (Swagger UI)

**Endpoints:**
- `/api/v1/auth/*` - Authentication (4 endpoints)
- `/api/v1/kpis/*` - KPI management (11 endpoints)
- `/api/v1/templates/*` - Templates (5 endpoints)
- `/health` - Health check

## Support

- Check `/docs/` for detailed documentation
- Review phase completion files for examples
- Run verification scripts: `./verify_phase1.sh`, `./verify_phase2.sh`
- remember to update the related documents in this project to reflect or matching with this project