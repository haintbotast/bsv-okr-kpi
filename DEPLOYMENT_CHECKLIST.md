# Deployment Checklist

## Overview
This checklist ensures all critical steps are completed during deployment to avoid common issues like missing database migrations, environment variables, or configuration changes.

## Pre-Deployment Checklist

### 1. Code Review
- [ ] All code changes reviewed and tested locally
- [ ] No hardcoded secrets or credentials in code
- [ ] All TODO comments addressed or documented
- [ ] Code follows project conventions (see CLAUDE.md)

### 2. Database Migrations
- [ ] **CRITICAL**: All new migration files created
  ```bash
  # Check if there are pending model changes
  docker compose exec backend alembic revision --autogenerate -m "description"
  ```
- [ ] Migration files reviewed for correctness
- [ ] Migration tested locally (upgrade + downgrade)
- [ ] Migration files committed to git

### 3. Dependencies
- [ ] Backend: `requirements.txt` updated if new packages added
- [ ] Frontend: `package.json` updated if new packages added
- [ ] Dependencies tested locally

### 4. Environment Variables
- [ ] `.env` file updated with new variables (if any)
- [ ] Production `.env` file verified
- [ ] No sensitive data in `.env.example`

### 5. Build & Test
- [ ] Backend builds successfully: `docker compose build backend`
- [ ] Frontend builds successfully: `docker compose build frontend`
- [ ] All tests pass: `pytest` (backend) and `npm test` (frontend)
- [ ] No console errors in browser

## Deployment Steps

### Step 1: Backup
```bash
# Backup database
cp data/database/kpi.db data/backups/kpi_$(date +%Y%m%d_%H%M%S).db

# Backup uploads
tar -czf data/backups/uploads_$(date +%Y%m%d_%H%M%S).tar.gz data/uploads/
```

### Step 2: Pull Latest Code
```bash
git pull origin main
```

### Step 3: Build Images
```bash
docker compose build backend frontend
```

### Step 4: Apply Database Migrations ⚠️ CRITICAL
```bash
# Check current migration version
docker compose exec backend alembic current

# Apply all pending migrations
docker compose exec backend alembic upgrade head

# Verify migration applied
docker compose exec backend alembic current
```

**Common Issues:**
- **Symptom**: "no such column" errors in backend logs
- **Cause**: Forgot to run `alembic upgrade head`
- **Fix**: Run migration command above, then restart backend

### Step 5: Restart Services
```bash
docker compose up -d backend frontend
```

### Step 6: Verify Health
```bash
# Check service status
docker compose ps

# Check backend health
curl http://localhost:8000/health

# Check backend logs for errors
docker compose logs backend --tail 50

# Check frontend logs for errors
docker compose logs frontend --tail 50
```

### Step 7: Smoke Test
- [ ] Can access frontend at http://localhost
- [ ] Can login with admin account
- [ ] Dashboard loads without errors
- [ ] Can create/edit/delete test data
- [ ] Check browser console for errors (F12)
- [ ] Check network tab for failed API calls

## Post-Deployment

### Monitor for Issues
```bash
# Watch backend logs in real-time
docker compose logs -f backend

# Watch for errors
docker compose logs backend | grep -i error

# Check database connections
docker compose exec backend python3 -c "from app.database import engine; print('DB OK') if engine.connect() else print('DB FAILED')"
```

### Rollback Procedure (if needed)
```bash
# Stop services
docker compose down

# Restore database backup
cp data/backups/kpi_YYYYMMDD_HHMMSS.db data/database/kpi.db

# Checkout previous git commit
git checkout <previous-commit-hash>

# Rebuild and restart
docker compose build
docker compose up -d

# Downgrade migrations if needed
docker compose exec backend alembic downgrade <previous-revision>
```

## Common Deployment Issues

### Issue 1: Migration Not Applied
**Symptoms:**
- Frontend shows "Failed to load data"
- Backend logs show: `sqlite3.OperationalError: no such column`
- API returns 500 Internal Server Error

**Solution:**
```bash
docker compose exec backend alembic upgrade head
docker compose restart backend
```

### Issue 2: Frontend Not Rebuilding
**Symptoms:**
- New features not appearing in UI
- Old code still running

**Solution:**
```bash
docker compose build frontend --no-cache
docker compose up -d frontend
```

### Issue 3: Environment Variables Not Loaded
**Symptoms:**
- Configuration errors
- Missing secrets

**Solution:**
```bash
docker compose down
docker compose up -d
# This forces reload of .env file
```

### Issue 4: Port Conflicts
**Symptoms:**
- Services fail to start
- "Address already in use" errors

**Solution:**
```bash
# Find process using port
sudo lsof -i :8000  # Backend
sudo lsof -i :80    # Frontend

# Kill process or change port in docker-compose.yml
```

## Automated Deployment Script

### deployment/deploy.sh
```bash
#!/bin/bash
set -e

echo "🚀 Starting deployment..."

# Step 1: Backup
echo "📦 Creating backup..."
./deployment/backup.sh

# Step 2: Pull latest code
echo "📥 Pulling latest code..."
git pull origin main

# Step 3: Build
echo "🏗️  Building images..."
docker compose build backend frontend

# Step 4: Apply migrations
echo "🗄️  Applying database migrations..."
docker compose exec backend alembic upgrade head

# Step 5: Restart services
echo "♻️  Restarting services..."
docker compose up -d backend frontend

# Step 6: Wait for health
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Step 7: Verify
echo "✅ Verifying deployment..."
if docker compose ps | grep -q "unhealthy"; then
    echo "❌ Deployment failed! Services unhealthy"
    exit 1
fi

echo "✅ Deployment successful!"
echo "📊 Service status:"
docker compose ps
```

## Phase-Specific Notes

### When Adding Database Migrations (Phase C.5, etc.)
1. **Always** create migration file first
2. **Always** test migration locally
3. **Always** run `alembic upgrade head` during deployment
4. **Always** verify migration in production before marking as complete

### When Adding New API Endpoints
1. Test endpoint with curl/Postman before frontend integration
2. Check authentication requirements
3. Verify response schema matches frontend expectations
4. Test with invalid/missing parameters

### When Updating Frontend Components
1. Check browser console for errors
2. Verify API calls in Network tab
3. Test with different user roles (admin/manager/employee)
4. Clear browser cache if seeing old code

## Checklist Templates

### For Code Changes
```
- [ ] Migration created and tested
- [ ] Backend builds without errors
- [ ] Frontend builds without errors
- [ ] No console errors
- [ ] All API endpoints return expected responses
- [ ] Changes documented in phase completion file
```

### For Bug Fixes
```
- [ ] Root cause identified
- [ ] Fix tested locally
- [ ] Regression tests added (if applicable)
- [ ] Migration applied (if DB changes)
- [ ] Services restarted
- [ ] Fix verified in production
```

### For New Features
```
- [ ] Backend endpoints implemented
- [ ] Database migrations created and applied
- [ ] Frontend components implemented
- [ ] Integration tested end-to-end
- [ ] Documentation updated
- [ ] Phase completion file updated
```

## Quick Reference Commands

```bash
# Check migration status
docker compose exec backend alembic current

# Apply all migrations
docker compose exec backend alembic upgrade head

# Rollback one migration
docker compose exec backend alembic downgrade -1

# View migration history
docker compose exec backend alembic history

# Rebuild and restart
docker compose build backend frontend && docker compose up -d

# Check logs
docker compose logs -f backend
docker compose logs -f frontend

# Service status
docker compose ps

# Health check
curl http://localhost:8000/health

# Database query
docker compose exec backend python3 -c "
from sqlalchemy import create_engine, inspect
engine = create_engine('sqlite:////data/database/kpi.db')
inspector = inspect(engine)
print(inspector.get_table_names())
"
```

## Prevention Strategies

### 1. Always Use This Checklist
Print this checklist or keep it open during deployment.

### 2. Automate with Scripts
Use `deployment/deploy.sh` to automate common steps.

### 3. Document Phase Completions
Update `PHASE_XXX_COMPLETE.md` files with:
- What was changed
- What migrations were added
- What to verify after deployment

### 4. Use Git Hooks
Create `.git/hooks/pre-push` to remind about migrations:
```bash
#!/bin/bash
echo "⚠️  Remember to:"
echo "1. Apply database migrations after push"
echo "2. Restart backend service"
echo "3. Verify deployment with smoke test"
```

## Contact & Support

If deployment issues persist:
1. Check logs: `docker compose logs backend | grep -i error`
2. Review this checklist
3. Check `CLAUDE.md` for architecture notes
4. Review phase completion files for recent changes
5. Check `SESSION_NOTES.md` for recent work

---

**Last Updated**: 2025-11-10
**Version**: 1.0
**Maintained By**: Development Team
