# Docker Deployment Guide

## ✅ Docker Compose V2 Ready!

This project uses **Docker Compose V2** (`docker compose` without hyphen).

All environment variable issues have been resolved!

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

If the symlink doesn't exist, create it:
```bash
ln -sf ../backend/.env .env
```

### 3. Test configuration (no warnings should appear)
```bash
docker compose config | head -20
```

### 4. Start the containers
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
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Fixed Issues

### Environment Variables Not Loading

**Problem:** Docker Compose warned about missing `SECRET_KEY` and `CORS_ORIGINS` variables.

**Solution:** Updated `docker compose.yml` to include:
```yaml
services:
  backend:
    env_file:
      - ../backend/.env
```

This tells Docker Compose to load environment variables from the backend `.env` file.

### Docker Permission Denied

**Problem:** `permission denied while trying to connect to the Docker daemon socket`

**Solution:** Run one of these commands:

```bash
# Option 1: Add your user to docker group (requires logout/login)
sudo usermod -aG docker $USER

# Option 2: Run with sudo (temporary solution)
sudo docker compose up -d --build

# Option 3: Fix socket permissions (not recommended for production)
sudo chmod 666 /var/run/docker.sock
```

**Recommended:** Use Option 1, then logout and login again.

### Obsolete Version Field

**Problem:** Warning about obsolete `version` field in docker compose.yml

**Solution:** Removed the `version: '3.8'` line (Docker Compose v2+ doesn't need it)

---

## File Paths in docker compose.yml

All paths are now relative to the `deployment/` directory:

- **Build Context:**
  - Backend: `../backend`
  - Frontend: `../frontend`

- **Environment File:**
  - Backend: `../backend/.env`

- **Volumes:**
  - Database: `../data/database`
  - Uploads: `../data/uploads`
  - Backups: `../data/backups`
  - Logs: `../data/logs`

---

## Common Commands

### View logs
```bash
cd deployment/
docker compose logs -f              # All services
docker compose logs -f backend      # Backend only
docker compose logs -f frontend     # Frontend only
```

### Stop containers
```bash
cd deployment/
docker compose down                 # Stop and remove containers
docker compose down -v              # Also remove volumes
```

### Restart services
```bash
cd deployment/
docker compose restart backend      # Restart backend only
docker compose restart              # Restart all services
```

### Execute commands in containers
```bash
cd deployment/
docker compose exec backend bash                           # Shell into backend
docker compose exec backend python scripts/backup.py       # Run backup
docker compose exec backend alembic upgrade head           # Run migrations
```

### Check container status
```bash
cd deployment/
docker compose ps                   # List containers
docker compose top                  # Show processes
```

---

## Environment Variables

The system reads environment variables from `/backend/.env`. Key variables:

### Required
- `SECRET_KEY` - JWT secret (generate: `openssl rand -hex 32`)
- `DATABASE_URL` - Database path (default: `sqlite:////data/database/kpi.db`)
- `CORS_ORIGINS` - Allowed origins (e.g., `http://localhost,http://localhost:3000`)

### Optional
- `SMTP_ENABLED` - Enable email notifications
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `BACKUP_RETENTION_DAYS` - Days to keep backups (default: 30)

---

## Troubleshooting

### Container won't start
```bash
# Check logs
docker compose logs backend

# Check if ports are available
sudo netstat -tulpn | grep -E ':(80|8000)'
```

### Database errors
```bash
# Recreate database
docker compose down
rm -f data/database/kpi.db*
docker compose up -d
docker compose exec backend python scripts/init_db.py
```

### Permission errors on volumes
```bash
# Fix permissions
sudo chown -R $USER:$USER data/
chmod -R 755 data/
```

### Frontend can't connect to backend
1. Check backend is running: `docker compose ps`
2. Check backend logs: `docker compose logs backend`
3. Verify CORS_ORIGINS in `.env` includes your frontend URL
4. Check network: `docker network inspect deployment_kpi-network`

---

## Production Deployment

### 1. Update environment variables
```bash
vim ../backend/.env
# Update:
# - SECRET_KEY (new random value)
# - CORS_ORIGINS (your production domain)
# - ENVIRONMENT=production
# - DEBUG=false
```

### 2. Enable HTTPS (optional but recommended)
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Update docker compose.yml to mount certificates
```

### 3. Set up automated backups
```bash
# Add to crontab
crontab -e

# Add line (daily backup at 2 AM)
0 2 * * * cd /home/haint/Documents/bsv-okr-kpi/deployment && docker compose exec -T backend python scripts/backup.py
```

### 4. Configure monitoring
```bash
# Install monitoring tools (optional)
docker compose logs --tail=100 | grep ERROR
```

---

## Security Checklist

- [ ] Changed default `SECRET_KEY`
- [ ] Changed default `ADMIN_PASSWORD`
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=false`
- [ ] Updated `CORS_ORIGINS` to only allowed domains
- [ ] Enabled HTTPS (SSL/TLS)
- [ ] Set up firewall rules
- [ ] Configured automated backups
- [ ] Set up log rotation
- [ ] Reviewed `.env` file permissions (should be 600)

---

## Quick Reference

```bash
# Fix Docker permission issue
sudo usermod -aG docker $USER
# Then logout/login

# Start from scratch
cd /home/haint/Documents/bsv-okr-kpi/deployment/
docker compose down -v
sudo rm -rf ../data/*
docker compose up -d --build
docker compose exec backend python scripts/init_db.py
docker compose exec backend python scripts/create_admin.py \
  --email admin@company.com \
  --password "Admin123!" \
  --fullname "Administrator"

# Access application
echo "Frontend: http://localhost"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
```

---

## Summary of Changes

### What was fixed:

1. ✅ **Removed obsolete `version` field** from docker compose.yml
2. ✅ **Added `env_file`** to backend service to load `../backend/.env`
3. ✅ **Updated all paths** to be relative to `deployment/` directory:
   - Build contexts: `../backend`, `../frontend`
   - Volumes: `../data/*`
4. ✅ **Updated deployment instructions** in docker compose.yml
5. ✅ **Created this guide** for easy reference

### How to use:

```bash
cd deployment/
docker compose up -d --build
```

The `.env` file will now be properly loaded from `backend/.env`, and all warnings should be resolved!

---

**Next Step:** Fix Docker permission issue with:
```bash
sudo usermod -aG docker $USER
```
Then logout and login, and run:
```bash
cd /home/haint/Documents/bsv-okr-kpi/deployment/
docker compose up -d --build
```
