# 🎯 KPI Management System - Complete Development Package

> **Lightweight, Self-Hosted KPI Management System**  
> Optimized for ~30 users | SQLite3 | Docker | Cost-Effective (~$150/year vs $2,500+/year for SaaS)

---

## 📦 What's Included

This package contains everything you need to build and deploy a production-ready KPI Management System:

1. **`CLAUDE_CODE_PROMPT_KPI_System.txt`** - Complete specification and instructions for Claude Code
2. **`QUICK_START_GUIDE.md`** - Step-by-step guide to use Claude Code
3. **`docker-compose.yml`** - Ready-to-use Docker deployment configuration
4. **`.env.example`** - Environment variables template with all settings
5. **This README** - Overview and quick reference

---

## 🚀 Quick Start (3 Steps)

### Step 1: Setup Project

```bash
# Create project directory
mkdir kpi-system
cd kpi-system

# Copy the provided files into the project directory
# - docker-compose.yml
# - .env.example

# Create .env from example
cp .env.example .env

# IMPORTANT: Edit .env and update these values:
# - SECRET_KEY (generate with: openssl rand -hex 32)
# - CORS_ORIGINS (add your domain)
# - ADMIN_EMAIL and ADMIN_PASSWORD
```

### Step 2: Build with Claude Code

```bash
# Start Claude Code in your project directory
claude-code

# In Claude Code, paste the entire CLAUDE_CODE_PROMPT_KPI_System.txt content
# Then say: "Build this system starting with Phase 1"

# Claude Code will create all the code!
```

### Step 3: Deploy

```bash
# Start the application
docker-compose up -d

# Initialize database
docker-compose exec backend python scripts/init_db.py

# Create admin user
docker-compose exec backend python scripts/create_admin.py \
  --email admin@company.com \
  --password "SecurePassword123!" \
  --fullname "System Admin"

# Access your application
# http://localhost (or your server IP)
```

---

## 🎯 System Overview

### Key Features

- ✅ **User Management** - Admin, Manager, Employee roles with RBAC
- ✅ **KPI Tracking** - Create, track, and manage KPIs by quarters (Q1-Q4)
- ✅ **File Management** - Upload evidence (PDF, Office docs, images)
- ✅ **Approval Workflow** - Submit → Review → Approve/Reject
- ✅ **Reporting** - Generate PDF/Excel reports
- ✅ **Dashboard** - Visual analytics and progress tracking
- ✅ **Comments** - Collaboration on KPIs
- ✅ **Notifications** - In-app notification system
- ✅ **Audit Log** - Track all activities
- ✅ **Automated Backup** - Daily database backups

### Technical Stack

**Backend:**
- FastAPI (Python 3.11+)
- SQLAlchemy ORM
- SQLite3 Database
- JWT Authentication
- APScheduler for background jobs

**Frontend:**
- React 18+
- Tailwind CSS
- Vite build tool
- Axios for API calls
- React Router for navigation

**Deployment:**
- Docker & Docker Compose
- Nginx reverse proxy
- Local file storage
- Single server deployment

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                     Users                           │
│              (Browsers/Mobile)                      │
└───────────────────────┬─────────────────────────────┘
                        │ HTTPS
                        ↓
┌─────────────────────────────────────────────────────┐
│              Nginx (Port 80/443)                    │
│         • Serves React Frontend                     │
│         • Proxies API to Backend                    │
│         • Serves uploaded files                     │
└───────────────────────┬─────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        ↓                               ↓
┌──────────────────┐          ┌──────────────────┐
│   Frontend       │          │    Backend       │
│   Container      │          │    Container     │
│   (React+Nginx)  │          │    (FastAPI)     │
│                  │          │                  │
│   Port: 80       │          │   Port: 8000     │
└──────────────────┘          └────────┬─────────┘
                                       │
                     ┌─────────────────┼─────────────────┐
                     ↓                 ↓                 ↓
              ┌───────────┐     ┌──────────┐     ┌──────────┐
              │  SQLite   │     │  Uploads │     │ Backups  │
              │  Database │     │   Files  │     │   Files  │
              │           │     │          │     │          │
              │  kpi.db   │     │  /data   │     │  /data   │
              └───────────┘     └──────────┘     └──────────┘
```

### File Structure (After Building with Claude Code)

```
kpi-system/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── api/
│   │   ├── crud/
│   │   └── services/
│   ├── scripts/
│   │   ├── init_db.py
│   │   ├── create_admin.py
│   │   └── backup.py
│   └── tests/
│
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── contexts/
│   └── public/
│
├── data/                    # Created automatically
│   ├── database/
│   │   └── kpi.db
│   ├── uploads/
│   ├── backups/
│   └── logs/
│
├── docker-compose.yml
├── .env
└── README.md
```

---

## 📖 Development Workflow

### Using Claude Code (Recommended)

1. **Open Claude Code** in your project directory
   ```bash
   claude-code
   ```

2. **Paste the prompt** from `CLAUDE_CODE_PROMPT_KPI_System.txt`

3. **Follow the phases:**
   - Phase 1: Core Infrastructure (Week 1)
   - Phase 2: KPI Management (Week 1)
   - Phase 3: File Management (Week 1)
   - Phase 4: Workflow & Collaboration (Week 1)
   - Phase 5: Reporting & Analytics (Week 1)
   - Phase 6: Admin Features (Week 1)
   - Phase 7: Optimization & Polish (Week 2)

4. **Test after each phase:**
   ```bash
   # Backend tests
   cd backend
   pytest
   
   # Frontend dev server
   cd frontend
   npm run dev
   
   # Full stack with Docker
   docker-compose up -d
   ```

### Manual Development (Without Claude Code)

If you prefer to code manually, the prompt file contains:
- Complete database schema
- API endpoint specifications
- Component structure
- Business logic requirements
- Security guidelines
- Best practices

---

## 🛠️ Common Commands

### Development

```bash
# Backend development
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend development
cd frontend
npm install
npm run dev

# Database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Docker Deployment

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# Execute commands in containers
docker-compose exec backend bash
docker-compose exec backend python scripts/backup.py
```

### Database Management

```bash
# Initialize database (first time)
docker-compose exec backend python scripts/init_db.py

# Create admin user
docker-compose exec backend python scripts/create_admin.py

# Backup database
docker-compose exec backend python scripts/backup.py
# Or manually:
cp data/database/kpi.db data/backups/kpi_$(date +%Y%m%d).db

# Restore database
docker-compose down
cp data/backups/kpi_YYYYMMDD.db data/database/kpi.db
docker-compose up -d

# Run migrations
docker-compose exec backend alembic upgrade head
```

---

## 🔒 Security Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` in `.env` (use `openssl rand -hex 32`)
- [ ] Update `ADMIN_PASSWORD` with a strong password
- [ ] Configure `CORS_ORIGINS` with your actual domain
- [ ] Set up HTTPS with Let's Encrypt
- [ ] Review file upload restrictions
- [ ] Enable automated backups
- [ ] Set up log rotation
- [ ] Configure firewall rules
- [ ] Change default ports (optional)
- [ ] Set up monitoring (optional)

---

## 📊 Cost Comparison

### DIY Solution (This System)

| Item | Cost | Note |
|------|------|------|
| VPS Server (2GB RAM, 2 CPU) | $12/month | DigitalOcean, Linode, Hetzner |
| Domain | $10/year | Namecheap, Cloudflare |
| SSL Certificate | Free | Let's Encrypt |
| **Total** | **~$154/year** | For unlimited users |

### SaaS Alternatives (30 users)

| Service | Cost/User/Month | Annual Cost (30 users) |
|---------|-----------------|------------------------|
| Perdoo | $8 | $2,880 |
| Weekdone | $7 | $2,520 |
| Quantive | $10 | $3,600 |

**💰 Savings: $2,366 - $3,446 per year (94-96% cheaper!)**

**ROI:**
- Development: 6-8 weeks (with Claude Code)
- Break-even: < 3 months
- Ongoing: Free (except server costs)

---

## 🎯 System Capacity

Optimized for:
- ✅ **30 users** (can scale to 100+ if needed)
- ✅ **5,000-10,000 KPIs** per year
- ✅ **50,000+ file uploads** (up to 50MB each)
- ✅ **100,000+ comments/notifications**

Database size estimate:
- Year 1: ~500 MB
- Year 2: ~1 GB
- Year 3: ~1.5 GB

Server resources:
- **CPU**: 2 cores (sufficient)
- **RAM**: 2GB (comfortable)
- **Disk**: 20GB SSD (ample space)
- **Network**: 10 Mbps

---

## 📱 User Roles & Permissions

### Admin
- Full system access
- Manage users
- Manage templates
- System settings
- View all KPIs
- Generate reports

### Manager
- Approve/reject team KPIs
- View team KPIs
- Create own KPIs
- Generate team reports
- Add comments

### Employee
- Create own KPIs
- Submit for approval
- Upload evidence
- Add comments
- View own dashboard
- Generate own reports

---

## 🔧 Troubleshooting

### Common Issues

**Issue: Cannot start containers**
```bash
# Check if ports are in use
sudo lsof -i :80
sudo lsof -i :8000

# Check Docker service
sudo systemctl status docker

# View container logs
docker-compose logs
```

**Issue: Database locked**
```bash
# Enable WAL mode (better for concurrency)
docker-compose exec backend python -c "
import sqlite3
conn = sqlite3.connect('/data/database/kpi.db')
conn.execute('PRAGMA journal_mode=WAL')
conn.close()
"
```

**Issue: File upload fails**
```bash
# Check permissions
docker-compose exec backend ls -la /data/uploads

# Fix permissions
docker-compose exec backend chmod 777 /data/uploads
```

**Issue: Frontend can't reach backend**
```bash
# Check CORS settings in .env
# Verify backend is running
curl http://localhost:8000/health

# Check Docker network
docker network inspect kpi-system_kpi-network
```

---

## 📚 Documentation

After building with Claude Code, you'll have:

1. **API Documentation** - Automatic Swagger UI at `/docs`
2. **User Guide** - In-app help and tooltips
3. **Admin Guide** - System administration documentation
4. **Technical Docs** - Code comments and README files

Access API docs:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app tests/
pytest -v tests/test_auth.py
```

### Frontend Tests (if implemented)

```bash
cd frontend
npm test
npm run test:e2e
```

### Manual Testing Checklist

- [ ] User can register/login
- [ ] User can create KPI
- [ ] User can upload files
- [ ] Manager can approve/reject
- [ ] Reports generate correctly
- [ ] Dashboard shows data
- [ ] Comments work
- [ ] Notifications appear
- [ ] Mobile responsive
- [ ] Works on Chrome, Firefox, Safari

---

## 🚀 Deployment to Production

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Step 2: Deploy Application

```bash
# Clone or copy your code to server
git clone your-repo-url kpi-system
cd kpi-system

# Configure environment
cp .env.example .env
nano .env  # Edit with production settings

# Start services
docker-compose up -d

# Initialize
docker-compose exec backend python scripts/init_db.py
docker-compose exec backend python scripts/create_admin.py
```

### Step 3: Setup SSL (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

### Step 4: Setup Backup Automation

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec backend python scripts/backup.py
echo "Backup completed: $DATE"
EOF

chmod +x backup.sh

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /path/to/kpi-system/backup.sh") | crontab -
```

---

## 📈 Monitoring (Optional)

### Basic Monitoring

```bash
# Check container health
docker-compose ps

# View resource usage
docker stats

# Check disk space
df -h

# View application logs
docker-compose logs --tail=100 -f backend
```

### Advanced Monitoring (Optional)

Consider adding:
- **Uptime Kuma** - Simple uptime monitoring
- **Grafana + Prometheus** - Detailed metrics
- **Sentry** - Error tracking
- **New Relic** - Application performance monitoring

---

## 🤝 Support & Contributing

### Getting Help

1. **Check the documentation** in the prompt file
2. **Search issues** in project repository (if using Git)
3. **Ask Claude Code** for clarification
4. **Review logs** for error messages

### Contributing

If you improve the system:
1. Document changes clearly
2. Update relevant documentation
3. Test thoroughly before deployment
4. Share improvements with your team

---

## 📝 Changelog

### Version 1.0.0 (Initial Release)
- Complete KPI management system
- User management with RBAC
- File upload and management
- Approval workflow
- Reporting (PDF/Excel)
- Dashboard with analytics
- Docker deployment
- Automated backups

---

## 📜 License

This project is provided as-is for internal company use. Customize as needed for your organization.

---

## 🎉 Ready to Build!

You now have everything needed to create your KPI Management System:

1. ✅ Complete specification (Prompt file)
2. ✅ Step-by-step guide (Quick Start Guide)
3. ✅ Ready-to-use Docker setup
4. ✅ Configuration templates
5. ✅ This comprehensive README

**Next Steps:**
1. Read the **QUICK_START_GUIDE.md**
2. Open **Claude Code** in your project directory
3. Paste the prompt from **CLAUDE_CODE_PROMPT_KPI_System.txt**
4. Start building! 🚀

**Estimated Timeline:**
- Setup: 1 hour
- Development with Claude Code: 6-8 weeks
- Testing & Deployment: 1 week
- **Total: ~8-9 weeks to production**

**Questions?** Review the documentation files or ask Claude Code for help!

---

**Good luck building your KPI Management System!** 💪

Made with ❤️ for IT Teams managing ~30 users
