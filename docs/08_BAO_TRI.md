# Bảo Trì & Troubleshooting - Hệ Thống Quản Lý KPI

---

## Nhiệm Vụ Bảo Trì

### Hàng Ngày
- [ ] Kiểm tra application logs
- [ ] Monitor disk space
- [ ] Verify backups completed

### Hàng Tuần
- [ ] Review error logs
- [ ] Check user feedback
- [ ] Update documentation (nếu cần)

### Hàng Tháng
- [ ] Update dependencies (security patches)
- [ ] Review và clean old backups
- [ ] Analyze usage statistics
- [ ] Performance review

### Hàng Quý
- [ ] Full security audit
- [ ] Update documentation
- [ ] Plan new features
- [ ] User training sessions

---

## Backup & Restore

### Manual Backup
```bash
# Backup database
docker-compose exec backend python scripts/backup.py

# Or manually
cp data/database/kpi.db data/backups/kpi_$(date +%Y%m%d_%H%M%S).db

# Backup uploads
tar -czf backups/uploads_$(date +%Y%m%d).tar.gz data/uploads/
```

### Restore
```bash
# Stop application
docker-compose down

# Restore database
cp data/backups/kpi_20240101_120000.db data/database/kpi.db

# Restore uploads
tar -xzf backups/uploads_20240101.tar.gz -C data/

# Start application
docker-compose up -d
```

---

## Common Issues & Solutions

### 1. Database Locked

**Triệu chứng**: Error "database is locked"

**Giải pháp**:
```bash
# Enable WAL mode
docker-compose exec backend python -c "
import sqlite3
conn = sqlite3.connect('/data/database/kpi.db')
conn.execute('PRAGMA journal_mode=WAL')
conn.close()
"

# Restart containers
docker-compose restart
```

### 2. Out of Disk Space

**Triệu chứng**: Uploads fail, database errors

**Giải pháp**:
```bash
# Check disk usage
df -h

# Clean old backups
find data/backups/ -type f -mtime +30 -delete

# Clean old logs
find data/logs/ -type f -mtime +7 -delete

# Clean Docker
docker system prune -a
```

### 3. Slow Performance

**Triệu chứng**: API response chậm, UI lag

**Giải pháp**:
```bash
# Check resource usage
docker stats

# Optimize database
docker-compose exec backend python -c "
import sqlite3
conn = sqlite3.connect('/data/database/kpi.db')
conn.execute('VACUUM')
conn.execute('ANALYZE')
conn.close()
"

# Restart containers
docker-compose restart
```

### 4. Cannot Login

**Triệu chứng**: Login fails, invalid credentials

**Giải pháp**:
```bash
# Reset user password
docker-compose exec backend python scripts/reset_password.py \
  --email user@company.com \
  --password NewPassword123!

# Check user status
docker-compose exec backend python -c "
from app.database import SessionLocal
from app.models import User
db = SessionLocal()
user = db.query(User).filter(User.email == 'user@company.com').first()
print(f'Active: {user.is_active}')
db.close()
"
```

### 5. File Upload Fails

**Triệu chứng**: Upload button doesn't work, 413 error

**Giải pháp**:
```bash
# Check permissions
docker-compose exec backend ls -la /data/uploads

# Fix permissions
docker-compose exec backend chmod 777 /data/uploads

# Check Nginx config (max upload size)
grep client_max_body_size nginx.prod.conf

# Increase if needed and restart
docker-compose restart frontend
```

### 6. Email Not Sending

**Triệu chứng**: Notifications not received

**Giải pháp**:
```bash
# Check SMTP settings in .env
cat .env | grep SMTP

# Test SMTP connection
docker-compose exec backend python -c "
import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('your-email@gmail.com', 'app-password')
print('SMTP connection successful')
server.quit()
"
```

---

## Logs

### View Logs
```bash
# All containers
docker-compose logs -f

# Specific container
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 backend

# Application logs
tail -f data/logs/app.log

# Nginx logs
docker-compose exec frontend tail -f /var/log/nginx/access.log
docker-compose exec frontend tail -f /var/log/nginx/error.log
```

### Log Rotation
```bash
# Setup logrotate
sudo cat > /etc/logrotate.d/kpi-system << 'EOF'
/path/to/kpi-system/data/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

---

## Performance Monitoring

### Check Performance
```bash
# Response time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/v1/kpis

# Database size
du -sh data/database/kpi.db

# Uploads size
du -sh data/uploads/

# Container resources
docker stats --no-stream
```

### Optimize Database
```bash
docker-compose exec backend python -c "
import sqlite3
conn = sqlite3.connect('/data/database/kpi.db')

# Compact database
conn.execute('VACUUM')

# Update statistics
conn.execute('ANALYZE')

# Check integrity
result = conn.execute('PRAGMA integrity_check').fetchone()
print(f'Integrity: {result[0]}')

conn.close()
"
```

---

## Security

### Update Packages
```bash
# Backend
docker-compose exec backend pip list --outdated
docker-compose exec backend pip install --upgrade <package>

# Frontend
docker-compose exec frontend npm outdated
docker-compose exec frontend npm update
```

### Review Logs for Suspicious Activity
```bash
# Failed login attempts
grep "401 Unauthorized" data/logs/app.log | tail -20

# File upload attempts
grep "upload" data/logs/app.log | grep -v "200"

# Large requests
grep "413" data/logs/nginx/access.log
```

---

## Support

### Collect Debug Info
```bash
# System info
uname -a
docker --version
docker-compose --version

# Container status
docker-compose ps

# Recent logs
docker-compose logs --tail=50

# Environment (sanitized)
cat .env | grep -v PASSWORD | grep -v SECRET
```

### Contact
- Email: support@company.com
- Documentation: https://github.com/your-org/kpi-system/docs

---

**Ghi nhớ**: Backup trước khi thay đổi quan trọng!
