# Docker Container Operations Guide

## Quick Reference Card

### 📍 Navigate to deployment directory first
```bash
cd /home/haint/Documents/bsv-okr-kpi/deployment
```

---

## 🚀 Basic Operations

### Start/Stop Containers

```bash
# Start containers
./deploy.sh start           # or ./deploy.sh up

# Stop containers
./deploy.sh stop

# Restart containers
./deploy.sh restart

# Restart specific service
./deploy.sh restart backend
./deploy.sh restart frontend
```

---

## 📊 Monitoring

### Check Container Status

```bash
# View running containers
./deploy.sh status          # or ./deploy.sh ps

# Output example:
# NAME           STATUS                    PORTS
# kpi-backend    Up (healthy)             0.0.0.0:8000->8000/tcp
# kpi-frontend   Up (healthy)             0.0.0.0:80->80/tcp
```

### View Logs

```bash
# All services (live tail)
./deploy.sh logs

# Specific service
./deploy.sh logs backend
./deploy.sh logs frontend

# Using docker compose directly
sg docker -c "docker compose logs -f"              # Follow all logs
sg docker -c "docker compose logs -f backend"      # Backend only
sg docker -c "docker compose logs --tail=100"      # Last 100 lines
```

---

## 🗄️ Database Operations

### Initialize Database (First Time Only)

```bash
./deploy.sh init
```

**What it does:**
- Creates all database tables
- Sets up indexes
- Prepares the system for first use

### Create Admin User

```bash
./deploy.sh admin
```

**Interactive prompts:**
- Email (default: admin@company.com)
- Full name (default: System Administrator)
- Password (required, hidden input)

### Backup Database

```bash
./deploy.sh backup
```

**Manual backup:**
```bash
# Copy database file with timestamp
timestamp=$(date +%Y%m%d_%H%M%S)
cp ../data/database/kpi.db ../data/backups/kpi_${timestamp}.db
```

### Restore Database

```bash
# Stop containers
./deploy.sh stop

# Restore from backup
cp ../data/backups/kpi_YYYYMMDD_HHMMSS.db ../data/database/kpi.db

# Start containers
./deploy.sh start
```

---

## 🐚 Shell Access

### Access Container Shell

```bash
# Backend container (Python/FastAPI)
./deploy.sh shell backend

# Frontend container (Nginx/Alpine)
./deploy.sh shell frontend
```

**Common commands inside backend shell:**
```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Run Python scripts
python scripts/init_db.py
python scripts/create_admin.py --email admin@test.com --password "Pass123!"

# Check Python packages
pip list

# Exit shell
exit
```

---

## 🔧 Troubleshooting

### Container Won't Start

```bash
# Check logs for errors
./deploy.sh logs backend

# Remove containers and rebuild
sg docker -c "docker compose down"
sg docker -c "docker compose up -d --build"
```

### Database Locked

```bash
# Restart backend
./deploy.sh restart backend
```

### Reset Everything

```bash
# ⚠️ WARNING: This deletes all data!
./deploy.sh clean          # Will ask for confirmation

# Manual cleanup
sg docker -c "docker compose down -v"
rm -f ../data/database/*.db*
```

---

## 📦 Updates & Maintenance

### Update Application Code

```bash
# Pull latest code
cd /home/haint/Documents/bsv-okr-kpi
git pull origin main

# Rebuild and restart
cd deployment
sg docker -c "docker compose down"
sg docker -c "docker compose up -d --build"

# Run database migrations (if any)
sg docker -c "docker compose exec backend alembic upgrade head"
```

### View Resource Usage

```bash
# Container stats
sg docker -c "docker stats kpi-backend kpi-frontend"

# Press Ctrl+C to exit
```

### Clean Up Old Images

```bash
# Remove unused images
sg docker -c "docker image prune -f"

# Remove all unused data (images, volumes, networks)
sg docker -c "docker system prune -a --volumes"
```

---

## 🌐 Accessing the Application

### Web Access

- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Test Health Check

```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost
```

---

## 🔐 Security Operations

### Change Admin Password

1. Login to the application
2. Go to Profile settings
3. Change password

**Or via shell:**
```bash
./deploy.sh shell backend
python scripts/change_password.py --email admin@company.com
```

### View Active Sessions

```bash
# Check backend logs for authentication
./deploy.sh logs backend | grep "login"
```

---

## 📁 Data Management

### Data Directories

All data is stored in: `/home/haint/Documents/bsv-okr-kpi/data/`

```
data/
├── database/    # SQLite database files
├── uploads/     # User uploaded files
├── backups/     # Database backups
└── logs/        # Application logs
```

### Check Disk Usage

```bash
cd /home/haint/Documents/bsv-okr-kpi
du -sh data/*

# Output example:
# 10M    data/database
# 25M    data/uploads
# 5M     data/backups
# 2M     data/logs
```

### Clean Old Backups

```bash
# Keep only last 30 days
find ../data/backups -name "kpi_*.db" -mtime +30 -delete
```

### Clean Old Logs

```bash
# Logs are auto-rotated by the system
# Manual cleanup if needed:
find ../data/logs -name "*.log" -mtime +90 -delete
```

---

## 🔄 Advanced Operations

### Run Database Migration

```bash
sg docker -c "docker compose exec backend alembic upgrade head"
```

### Run Custom Python Script

```bash
sg docker -c "docker compose exec backend python /path/to/script.py"
```

### Export Database to SQL

```bash
sg docker -c "docker compose exec backend sqlite3 /data/database/kpi.db .dump" > backup.sql
```

### Import SQL to Database

```bash
cat backup.sql | sg docker -c "docker compose exec -T backend sqlite3 /data/database/kpi.db"
```

---

## 🚨 Emergency Procedures

### Application Not Responding

```bash
# 1. Check container status
./deploy.sh status

# 2. Check logs for errors
./deploy.sh logs backend

# 3. Restart containers
./deploy.sh restart

# 4. If still not working, rebuild
sg docker -c "docker compose down"
sg docker -c "docker compose up -d --build"
```

### Database Corrupted

```bash
# 1. Stop containers
./deploy.sh stop

# 2. Restore from backup
cp ../data/backups/kpi_LATEST.db ../data/database/kpi.db

# 3. Start containers
./deploy.sh start

# 4. Verify
curl http://localhost:8000/health
```

### Disk Full

```bash
# Check disk space
df -h

# Clean Docker system
sg docker -c "docker system prune -a --volumes -f"

# Clean old backups
find ../data/backups -name "*.db" -mtime +30 -delete

# Clean old logs
find ../data/logs -name "*.log" -mtime +90 -delete
```

---

## 📋 Automated Tasks

### Set Up Automated Backups

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * cd /home/haint/Documents/bsv-okr-kpi/deployment && ./deploy.sh backup

# Add weekly cleanup at Sunday 3 AM
0 3 * * 0 find /home/haint/Documents/bsv-okr-kpi/data/backups -name "kpi_*.db" -mtime +30 -delete
```

### Monitor Container Health

```bash
# Add to crontab for email alerts
*/5 * * * * cd /home/haint/Documents/bsv-okr-kpi/deployment && sg docker -c "docker compose ps" | grep -q "unhealthy" && echo "Container unhealthy!" | mail -s "Alert: KPI System" admin@company.com
```

---

## 📞 Getting Help

### View All Available Commands

```bash
./deploy.sh help
```

### Check Documentation

- `DOCKER_OPERATIONS.md` - This file (operations guide)
- `DOCKER_DEPLOYMENT.md` - Deployment guide
- `deployment/README.md` - Docker Compose V2 guide
- `DEPLOYMENT_SUCCESS.md` - Session summary
- `CLAUDE.md` - Project architecture

### Common Issues

**Port already in use:**
```bash
# Check what's using port 80 or 8000
sudo lsof -i :80
sudo lsof -i :8000

# Stop the conflicting service or change ports in docker-compose.yml
```

**Permission denied:**
```bash
# Make sure you're in the docker group
groups | grep docker

# If not, run: sudo usermod -aG docker $USER
# Then logout and login
```

**Cannot connect to Docker daemon:**
```bash
# Use sg docker -c wrapper
sg docker -c "docker compose ps"

# Or logout/login to refresh groups
```

---

## 🎯 Quick Command Summary

| Task | Command |
|------|---------|
| Start | `./deploy.sh start` |
| Stop | `./deploy.sh stop` |
| Restart | `./deploy.sh restart` |
| Status | `./deploy.sh status` |
| Logs | `./deploy.sh logs` |
| Shell | `./deploy.sh shell` |
| Backup | `./deploy.sh backup` |
| Init DB | `./deploy.sh init` |
| Create Admin | `./deploy.sh admin` |
| Help | `./deploy.sh help` |

---

## ✅ Daily Operations Checklist

### Morning Check
- [ ] Check container status: `./deploy.sh status`
- [ ] Review overnight logs: `./deploy.sh logs backend | tail -100`
- [ ] Check disk space: `df -h`

### Weekly Maintenance
- [ ] Review backups: `ls -lh ../data/backups/`
- [ ] Clean old backups (>30 days)
- [ ] Check resource usage: `sg docker -c "docker stats"`

### Monthly Tasks
- [ ] Update system: `git pull && ./deploy.sh stop && ./deploy.sh start --build`
- [ ] Review user accounts
- [ ] Clean old uploaded files
- [ ] Test backup restoration

---

**For detailed deployment instructions, see:** `DOCKER_DEPLOYMENT.md`
**For troubleshooting, see:** `deployment/PERMISSIONS_FIXED.md`
