# Project Overview - KPI Management System

**Version**: 1.0.0
**Target Scale**: ~30 users
**Tech Stack**: FastAPI + React + SQLite3 + Docker
**Deployment**: Single server, self-hosted

---

## Purpose

Build a complete, production-ready KPI (Key Performance Indicator) Management System optimized for small teams (~30 users). The system must be:

- ✓ **Self-contained** (SQLite database, local file storage)
- ✓ **Easy to deploy** (Docker Compose, 2 containers only)
- ✓ **Cost-effective** (no external services required)
- ✓ **Secure** (JWT auth, bcrypt passwords, RBAC)
- ✓ **User-friendly** (modern UI, responsive design)
- ✓ **Maintainable** (clean code, documented, tested)

---

## Target Users

### User Breakdown (~30 users total):
- **IT Department**: 5-10 users
- **Management Team**: 3-5 users
- **Department Staff**: 15-20 users

### User Roles:
1. **Admin**
   - Full system access
   - Manage users and templates
   - System configuration
   - View all KPIs

2. **Manager**
   - Approve/reject team KPIs
   - View team KPIs
   - Create own KPIs
   - Generate team reports

3. **Employee**
   - Create own KPIs
   - Submit for approval
   - Upload evidence
   - Generate own reports

---

## Business Requirements

### Core Features:
1. **Manage KPIs by quarters** (Q1-Q4) per year
2. **Track progress** with evidence uploads
3. **Support approval workflow** (Submit → Review → Approve/Reject)
4. **Generate reports** (PDF/Excel export)
5. **Role-based access control** (Admin, Manager, Employee)
6. **Comment and collaboration** features

### KPI Categories:
- **Mission** (Nhiệm vụ): Long-term strategic goals
- **Goal** (Mục tiêu): Specific measurable objectives
- **Task** (Công việc): Actionable work items

### Measurement Types:
- **Percentage** (e.g., 99.9% uptime)
- **Number** (e.g., 100 sales)
- **Boolean** (e.g., completed/not completed)

---

## Cost Comparison

### DIY Solution (This System):
| Item | Cost | Annual Cost |
|------|------|-------------|
| VPS Server (2GB RAM, 2 CPU) | $12/month | $144/year |
| Domain | - | $10/year |
| SSL Certificate | Free (Let's Encrypt) | $0 |
| **Total** | | **~$154/year** |

**For unlimited users!**

### SaaS Alternatives (30 users):
| Service | Cost/User/Month | Annual Cost (30 users) |
|---------|-----------------|------------------------|
| Perdoo | $8 | $2,880/year |
| Weekdone | $7 | $2,520/year |
| Quantive | $10 | $3,600/year |

### Savings:
- **$2,366 - $3,446 per year** (94-96% cheaper!)
- **Break-even**: < 3 months of development
- **ROI**: Ongoing savings year after year

---

## System Capacity

Designed for:
- ✅ **30 users** (can scale to 100+ if needed)
- ✅ **5,000-10,000 KPIs** per year
- ✅ **50,000+ file uploads** (up to 50MB each)
- ✅ **100,000+ comments/notifications**

### Database Size Estimate:
- **Year 1**: ~500 MB
- **Year 2**: ~1 GB
- **Year 3**: ~1.5 GB

### Server Resources:
- **CPU**: 2 cores (sufficient)
- **RAM**: 2GB (comfortable)
- **Disk**: 20GB SSD (ample space)
- **Network**: 10 Mbps

---

## Development Timeline

### 7-Phase Development Plan:

| Phase | Focus | Time |
|-------|-------|------|
| **Phase 1** | Core Infrastructure | Week 1 |
| **Phase 2** | KPI Management | Week 2 |
| **Phase 3** | File Management | Week 3 |
| **Phase 4** | Workflow & Collaboration | Week 4 |
| **Phase 5** | Reporting & Analytics | Week 5 |
| **Phase 6** | Admin Features | Week 6 |
| **Phase 7** | Optimization & Polish | Week 7-8 |

**Total Estimated Timeline**: 6-8 weeks
**Estimated Effort**: 200-240 hours

---

## Key Features

### User Management
- User registration (can be disabled)
- JWT authentication
- Role-based access control (RBAC)
- Password reset
- Profile management

### KPI Management
- Create KPIs from templates
- Track by year and quarter
- Progress tracking
- Status workflow (draft → submitted → approved/rejected)
- Search and filter
- History/audit trail

### File Management
- Upload evidence (PDF, Office docs, images)
- Max 50MB per file
- File preview
- Secure file storage
- Download files

### Approval Workflow
- Submit KPI for approval
- Manager review
- Approve with comments
- Reject with reason
- Notification system

### Reporting
- PDF reports
- Excel exports
- User reports
- Department reports
- Company-wide reports (Admin)
- Custom date ranges

### Dashboard & Analytics
- Overview statistics
- Progress by quarter
- Charts and visualizations
- Department comparison
- Completion rates

### Collaboration
- Comments on KPIs
- Activity timeline
- Notifications
- Real-time updates (polling)

### Admin Features
- User management
- Template management
- System settings
- Backup management
- Audit log

### Automated Tasks
- Daily backups (2 AM)
- Cleanup old notifications
- Email reminders (optional)
- Log rotation

---

## Technical Philosophy

### Keep It Simple:
This system is designed for **30 users**, not 30,000. We prioritize:

1. **Simplicity** over scalability
2. **Maintainability** over features
3. **Cost-effectiveness** over performance
4. **Self-contained** over distributed

### What We DON'T Use:
- ❌ PostgreSQL/MySQL (SQLite is enough)
- ❌ Redis (in-memory caching not needed)
- ❌ Celery/RabbitMQ (APScheduler is sufficient)
- ❌ S3/MinIO (local storage works fine)
- ❌ Kubernetes (Docker Compose is enough)
- ❌ Microservices (monolith is simpler)

### What We DO Use:
- ✅ SQLite3 (simple, reliable, ACID compliant)
- ✅ Local file storage (direct, fast)
- ✅ APScheduler (in-process background jobs)
- ✅ Docker Compose (easy deployment)
- ✅ JWT tokens (stateless auth)
- ✅ Nginx (reverse proxy + file serving)

---

## Success Metrics

### Technical Metrics:
- ✅ System uptime: >99%
- ✅ Page load time: <3 seconds
- ✅ API response time: <500ms
- ✅ Database size: <500MB (first year)
- ✅ Zero data loss
- ✅ Zero security breaches

### Business Metrics:
- ✅ User adoption: 100% of target users
- ✅ KPI completion rate: >80% on time
- ✅ User satisfaction: >4/5 rating
- ✅ Support tickets: <10 per month
- ✅ Training time: <2 hours per user

---

## Documentation Structure

This documentation is organized as follows:

1. **01_OVERVIEW.md** (this file) - Project overview
2. **02_ARCHITECTURE.md** - System architecture and design
3. **03_DATABASE_SCHEMA.md** - Database structure
4. **04_FEATURES_PHASES.md** - Features by development phase
5. **05_SECURITY.md** - Security best practices
6. **06_TESTING.md** - Testing strategy
7. **07_DEPLOYMENT.md** - Deployment guide
8. **08_MAINTENANCE.md** - Maintenance procedures
9. **API_SPECIFICATION.md** - Complete API documentation

---

## Quick Links

- [Main README](../README.md) - Quick start guide
- [Quick Start Guide](../QUICK_START_GUIDE.md) - How to use Claude Code
- [Architecture](./02_ARCHITECTURE.md) - System design
- [Database Schema](./03_DATABASE_SCHEMA.md) - Database structure
- [API Specification](./API_SPECIFICATION.md) - API documentation
- [Docker Compose](../docker-compose.yml) - Deployment configuration

---

## Getting Started

Ready to build? Follow these steps:

1. Read the [QUICK_START_GUIDE.md](../QUICK_START_GUIDE.md)
2. Review the [Architecture](./02_ARCHITECTURE.md)
3. Study the [Database Schema](./03_DATABASE_SCHEMA.md)
4. Start building with Phase 1!

---

**Let's build an amazing KPI Management System!** 🚀
