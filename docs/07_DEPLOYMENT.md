# Hướng Dẫn Deployment - Hệ Thống Quản Lý KPI

---

## Deployment Lần Đầu

### 1. Chuẩn Bị Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker --version
docker-compose --version
```

### 2. Clone Repository

```bash
git clone https://github.com/your-org/kpi-system.git
cd kpi-system
```

### 3. Configure Environment

```bash
# Tạo .env từ template
cp .env.example .env

# Chỉnh sửa .env
nano .env

# QUAN TRỌNG: Thay đổi các giá trị sau
# - SECRET_KEY (openssl rand -hex 32)
# - ADMIN_PASSWORD
# - CORS_ORIGINS (domain của bạn)
```

### 4. Deploy với Docker

```bash
# Development
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d --build
```

### 5. Initialize Database

```bash
# Tạo tables
docker-compose exec backend python scripts/init_db.py

# Tạo admin user
docker-compose exec backend python scripts/create_admin.py \
  --email admin@company.com \
  --password "SecurePassword123!" \
  --fullname "Quản Trị Viên"
```

### 6. Kiểm Tra

```bash
# Check containers
docker-compose ps

# Check logs
docker-compose logs -f

# Test API
curl http://localhost:8000/health

# Test frontend
curl http://localhost
```

---

## Setup SSL/HTTPS (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

---

## Setup Automated Backups

```bash
# Tạo backup script
cat > /home/user/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cd /path/to/kpi-system
docker-compose exec -T backend python scripts/backup.py
echo "Backup completed: $DATE"
EOF

chmod +x /home/user/backup.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /home/user/backup.sh >> /var/log/kpi-backup.log 2>&1") | crontab -
```

---

## Update Application

```bash
# Pull latest code
git pull origin main

# Stop services
docker-compose down

# Rebuild and start
docker-compose up -d --build

# Run migrations
docker-compose exec backend alembic upgrade head

# Check status
docker-compose ps
docker-compose logs -f
```

---

## Rollback

```bash
# Checkout previous version
git log --oneline  # Find commit hash
git checkout <commit-hash>

# Rebuild
docker-compose down
docker-compose up -d --build

# Restore database if needed
docker-compose down
cp data/backups/kpi_YYYYMMDD.db data/database/kpi.db
docker-compose up -d
```

---

## Monitoring

```bash
# View logs
docker-compose logs -f backend
docker-compose logs --tail=100 backend

# Check resource usage
docker stats

# Check disk space
df -h
```

---

## Troubleshooting

### Issue: Containers không start
```bash
# Check ports
sudo lsof -i :80
sudo lsof -i :8000

# Check Docker service
sudo systemctl status docker

# View logs
docker-compose logs
```

### Issue: Database locked
```bash
# Enable WAL mode
docker-compose exec backend python -c "
import sqlite3
conn = sqlite3.connect('/data/database/kpi.db')
conn.execute('PRAGMA journal_mode=WAL')
conn.close()
"
```

### Issue: File upload fails
```bash
# Check permissions
docker-compose exec backend ls -la /data/uploads

# Fix permissions
docker-compose exec backend chmod 777 /data/uploads
```

---

## Production Checklist

- [ ] Environment variables configured
- [ ] Strong SECRET_KEY set
- [ ] HTTPS enabled
- [ ] Firewall configured (ports 80, 443 only)
- [ ] Automated backups setup
- [ ] Log rotation configured
- [ ] Monitoring setup
- [ ] Database initialized
- [ ] Admin user created
- [ ] Test all features work
- [ ] Backup tested and verified

---

**Server Requirements**:
- CPU: 2 cores
- RAM: 2GB
- Disk: 20GB SSD
- OS: Ubuntu 22.04 LTS
