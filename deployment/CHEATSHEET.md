# Docker Operations Cheat Sheet

## 📍 ALWAYS START HERE
```bash
cd /home/haint/Documents/bsv-okr-kpi/deployment
```

---

## ⚡ Most Common Commands

```bash
# View status
./deploy.sh status

# View logs (live)
./deploy.sh logs

# Restart everything
./deploy.sh restart

# Stop everything
./deploy.sh stop

# Start everything
./deploy.sh start
```

---

## 🆘 Emergency Commands

```bash
# Not working? Restart!
./deploy.sh restart

# Still not working? Rebuild!
sg docker -c "docker compose down"
sg docker -c "docker compose up -d --build"

# Check what's wrong
./deploy.sh logs backend
```

---

## 🗄️ Database Commands

```bash
# First time setup
./deploy.sh init              # Initialize database
./deploy.sh admin             # Create admin user

# Backup
./deploy.sh backup            # Create backup

# Access database
./deploy.sh shell backend     # Then run: sqlite3 /data/database/kpi.db
```

---

## 🔍 Debugging Commands

```bash
# View live logs
./deploy.sh logs backend      # Backend logs
./deploy.sh logs frontend     # Frontend logs

# Check if running
./deploy.sh status

# Get into container
./deploy.sh shell backend     # Backend shell
./deploy.sh shell frontend    # Frontend shell
```

---

## 🌐 Access URLs

- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

---

## 📦 Update Application

```bash
cd /home/haint/Documents/bsv-okr-kpi
git pull
cd deployment
./deploy.sh stop
./deploy.sh start
```

---

## 🧹 Cleanup Commands

```bash
# Remove containers (keeps data)
sg docker -c "docker compose down"

# Remove everything (⚠️ DELETES DATA!)
./deploy.sh clean

# Clean old Docker images
sg docker -c "docker image prune -f"
```

---

## 📊 Monitoring

```bash
# Resource usage
sg docker -c "docker stats kpi-backend kpi-frontend"

# Disk space
du -sh ../data/*

# Check health
curl http://localhost:8000/health
```

---

## 🔐 User Management

```bash
# Create admin (interactive)
./deploy.sh admin

# Via shell
./deploy.sh shell backend
python scripts/create_admin.py \
  --email admin@test.com \
  --password "Pass123!" \
  --fullname "Admin"
```

---

## ❓ Get Help

```bash
# Show all commands
./deploy.sh help

# Read full guide
cat ../DOCKER_OPERATIONS.md
```

---

## 📁 Important Directories

```
/home/haint/Documents/bsv-okr-kpi/
├── deployment/           # ← Work from here
│   ├── deploy.sh        # ← Main script
│   └── docker-compose.yml
├── data/
│   ├── database/        # Database files
│   ├── uploads/         # User files
│   ├── backups/         # Backups
│   └── logs/            # Logs
└── backend/.env         # Config file
```

---

## 🚦 Traffic Light System

### 🟢 Everything OK
```bash
./deploy.sh status
# Both show: Up (healthy)
```

### 🟡 Warning
```bash
./deploy.sh logs
# Check for warnings
```

### 🔴 Error
```bash
./deploy.sh restart
# If still red, check logs
./deploy.sh logs backend
```

---

## 💡 Pro Tips

1. **Always check status first:** `./deploy.sh status`
2. **Logs are your friend:** `./deploy.sh logs`
3. **When in doubt, restart:** `./deploy.sh restart`
4. **Backup before updates:** `./deploy.sh backup`
5. **Test on health endpoint:** `curl http://localhost:8000/health`

---

**Need more details? Read:** `DOCKER_OPERATIONS.md`
