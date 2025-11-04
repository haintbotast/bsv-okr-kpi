# Docker Compose V2 Deployment Guide

## ✅ Fixed Issues

All environment variable warnings have been resolved!

### What was done:
1. ✅ Created symlink: `deployment/.env` → `../backend/.env`
2. ✅ Removed obsolete `version` field from docker-compose.yml
3. ✅ Updated all paths to be relative to deployment directory
4. ✅ Docker Compose V2 now automatically loads `.env` from current directory

---

## Quick Start

### 1. Navigate to deployment directory
```bash
cd /home/haint/Documents/bsv-okr-kpi/deployment/
```

### 2. Verify environment file (should show symlink)
```bash
ls -la .env
# Output: .env -> ../backend/.env
```

### 3. Test configuration (no warnings should appear)
```bash
docker compose config | head -20
```

### 4. Start the application
```bash
docker compose up -d --build
```

### 5. Initialize database (first time only)
```bash
docker compose exec backend python scripts/init_db.py
```

### 6. Create admin user (first time only)
```bash
docker compose exec backend python scripts/create_admin.py \
  --email admin@company.com \
  --password "SecurePassword123!" \
  --fullname "System Administrator"
```

### 7. Access the application
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Understanding Docker Compose V2

### Key Differences from V1:
- Command: `docker compose` (without hyphen) instead of `docker-compose`
- Automatically loads `.env` from the **directory where you run the command**
- No longer needs `version` field in docker-compose.yml
- Better integration with Docker CLI

### Environment Variable Loading:
```
deployment/
├── .env              ← Docker Compose V2 reads from here (symlink to ../backend/.env)
└── docker-compose.yml
```

---

## Common Commands

### Starting and Stopping
```bash
cd deployment/

# Start all services
docker compose up -d

# Start with rebuild
docker compose up -d --build

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v
```

### Viewing Logs
```bash
cd deployment/

# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend

# Last 100 lines
docker compose logs --tail=100 backend
```

### Service Management
```bash
cd deployment/

# List running services
docker compose ps

# Restart services
docker compose restart
docker compose restart backend

# Execute commands
docker compose exec backend bash
docker compose exec backend python scripts/backup.py
```

### Monitoring
```bash
cd deployment/

# Show resource usage
docker compose top

# Show container stats
docker stats kpi-backend kpi-frontend
```

---

## Environment Variables

The `.env` file in the deployment directory is a symlink to `../backend/.env`.

### Key Variables:
```bash
# Security (MUST CHANGE)
SECRET_KEY=your-secret-key-here          # Generate: openssl rand -hex 32

# CORS (Update for production)
CORS_ORIGINS=http://localhost,http://localhost:3000

# Database
DATABASE_URL=sqlite:////data/database/kpi.db

# Admin (Change after first login)
ADMIN_EMAIL=admin@company.com
ADMIN_PASSWORD=ChangeMe123!

# Optional Features
SMTP_ENABLED=false                       # Set true for email notifications
LOG_LEVEL=INFO                           # DEBUG, INFO, WARNING, ERROR
```

### Editing Environment Variables:
```bash
# Option 1: Edit the symlinked file
vim deployment/.env

# Option 2: Edit the original file
vim backend/.env

# Both edit the same file!
```

---

## Troubleshooting

### Issue: "variable is not set" warnings

**Cause**: `.env` file not in the deployment directory

**Solution**:
```bash
cd deployment/
ls -la .env
# Should show: .env -> ../backend/.env

# If missing, recreate symlink:
ln -sf ../backend/.env .env
```

### Issue: Docker permission denied

**Cause**: User not in docker group

**Solution**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again, then:
docker compose up -d
```

### Issue: Port already in use

**Cause**: Another service using port 80 or 8000

**Solution**:
```bash
# Check what's using the port
sudo lsof -i :80
sudo lsof -i :8000

# Kill the process or change ports in docker-compose.yml
```

### Issue: Container won't start

**Solution**:
```bash
cd deployment/

# Check logs
docker compose logs backend
docker compose logs frontend

# Check status
docker compose ps

# Restart from scratch
docker compose down -v
docker compose up -d --build
```

### Issue: Database locked

**Cause**: SQLite doesn't handle concurrent writes well

**Solution**:
```bash
# Restart backend service
docker compose restart backend

# Or check if multiple backends are running
docker ps | grep backend
```

### Issue: Frontend shows API errors

**Solution**:
```bash
# 1. Check backend is running
docker compose ps

# 2. Check backend logs
docker compose logs backend

# 3. Verify CORS settings in .env
cat .env | grep CORS_ORIGINS

# 4. Check network connectivity
docker compose exec frontend curl http://backend:8000/health
```

---

## File Structure

```
deployment/
├── .env                    # Symlink to ../backend/.env
├── docker-compose.yml      # Main compose file
├── docker-compose.prod.yml # Production overrides
├── nginx.prod.conf         # Nginx config
└── README.md              # This file

../backend/
├── .env                    # Environment variables (original)
├── Dockerfile
└── app/

../frontend/
├── Dockerfile
└── src/

../data/
├── database/              # SQLite database files
├── uploads/               # User uploaded files
├── backups/               # Database backups
└── logs/                  # Application logs
```

---

## Production Deployment

### 1. Update environment variables
```bash
cd deployment/
vim .env

# Update these values:
SECRET_KEY=<generate-new-with-openssl-rand-hex-32>
CORS_ORIGINS=https://your-domain.com
ENVIRONMENT=production
DEBUG=false
```

### 2. Deploy
```bash
cd deployment/
docker compose down
docker compose up -d --build
```

### 3. Initialize (first time only)
```bash
docker compose exec backend python scripts/init_db.py
docker compose exec backend python scripts/create_admin.py \
  --email admin@your-domain.com \
  --password "YourSecurePassword123!" \
  --fullname "System Administrator"
```

### 4. Verify
```bash
# Check all services are running
docker compose ps

# Check logs for errors
docker compose logs --tail=50

# Test frontend
curl http://localhost

# Test backend
curl http://localhost:8000/health
```

### 5. Set up automated backups
```bash
# Add to crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * cd /home/haint/Documents/bsv-okr-kpi/deployment && docker compose exec -T backend python scripts/backup.py
```

---

## Security Checklist

Before production deployment:

- [ ] Generate new `SECRET_KEY` (don't use example value)
- [ ] Change `ADMIN_PASSWORD` from default
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=false`
- [ ] Update `CORS_ORIGINS` to your production domain only
- [ ] Review file permissions: `chmod 600 .env`
- [ ] Enable HTTPS (SSL/TLS) with reverse proxy
- [ ] Set up firewall rules
- [ ] Configure automated backups
- [ ] Set up log rotation
- [ ] Test backup restoration procedure
- [ ] Enable monitoring/alerting

---

## Updating the Application

```bash
cd /home/haint/Documents/bsv-okr-kpi/deployment/

# Pull latest code
git pull origin main

# Rebuild and restart
docker compose down
docker compose up -d --build

# Run database migrations (if any)
docker compose exec backend alembic upgrade head

# Verify
docker compose ps
docker compose logs --tail=50
```

---

## Backup and Restore

### Backup
```bash
cd deployment/

# Using backup script
docker compose exec backend python scripts/backup.py

# Manual backup
timestamp=$(date +%Y%m%d_%H%M%S)
cp ../data/database/kpi.db ../data/backups/kpi_${timestamp}.db
```

### Restore
```bash
cd deployment/

# Stop services
docker compose down

# Restore database
cp ../data/backups/kpi_YYYYMMDD_HHMMSS.db ../data/database/kpi.db

# Start services
docker compose up -d

# Verify
docker compose logs backend
```

---

## Performance Tuning

### For 30 users (default):
```bash
# In .env
WORKERS=2
MAX_CONNECTIONS=100
CACHE_TIMEOUT=300
```

### For 50-100 users:
```bash
# In .env
WORKERS=4
MAX_CONNECTIONS=200
CACHE_TIMEOUT=600

# Consider upgrading server resources:
# - CPU: 2+ cores
# - RAM: 4GB+
# - Disk: SSD recommended
```

### For 100+ users:
```bash
# Consider migrating to PostgreSQL
# Update in .env:
DATABASE_URL=postgresql://user:pass@db:5432/kpi

# Add PostgreSQL to docker-compose.yml
```

---

## Monitoring

### Check container health
```bash
cd deployment/
docker compose ps
```

### View resource usage
```bash
docker stats kpi-backend kpi-frontend
```

### Check logs for errors
```bash
docker compose logs --tail=100 | grep -i error
docker compose logs --tail=100 | grep -i warning
```

### Database size
```bash
ls -lh ../data/database/kpi.db
```

### Disk usage
```bash
du -sh ../data/*
```

---

## Quick Reference

```bash
# Navigate to deployment directory (ALWAYS START HERE)
cd /home/haint/Documents/bsv-okr-kpi/deployment/

# Check configuration
docker compose config | less

# Start
docker compose up -d --build

# Stop
docker compose down

# Logs
docker compose logs -f backend

# Shell access
docker compose exec backend bash
docker compose exec frontend sh

# Restart
docker compose restart backend

# Status
docker compose ps

# Access points
echo "Frontend: http://localhost"
echo "Backend: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
```

---

## Support

If you encounter issues:

1. Check logs: `docker compose logs backend`
2. Verify config: `docker compose config`
3. Check environment: `cat .env | grep SECRET_KEY`
4. Review this README
5. Check main documentation in `/docs` directory

---

**Status**: ✅ All environment variable issues resolved!

The system is ready for deployment with Docker Compose V2.
