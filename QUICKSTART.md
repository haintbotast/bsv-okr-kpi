# Quick Start Guide - KPI Management System

**Status**: Phase 1 ✅ + Phase 2 ✅ Complete
**Ready to use**: YES

---

## 🚀 5-Minute Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git

### Step 1: Clone & Setup Backend (2 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Generate a secret key
openssl rand -hex 32
# Copy the output and paste it in .env as SECRET_KEY

# Create data directories
mkdir -p ../data/{database,uploads,backups,logs}

# Run migrations
alembic upgrade head

# Create admin user
python scripts/create_admin.py \
  --email admin@company.com \
  --password Admin123! \
  --fullname "System Admin"

# Start backend server
uvicorn app.main:app --reload
```

**Backend running at**: http://localhost:8000
**API Docs**: http://localhost:8000/docs

### Step 2: Setup Frontend (2 minutes)

```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Start dev server
npm run dev
```

**Frontend running at**: http://localhost:3000

### Step 3: Login & Test (1 minute)

1. Open browser: http://localhost:3000
2. Login with:
   - Email: `admin@company.com`
   - Password: `Admin123!`
3. You should see the Dashboard!

---

## 🎯 What You Can Do Now

### As Admin
- ✅ View dashboard with statistics
- ✅ Create KPI templates
- ✅ Create KPIs
- ✅ Edit draft KPIs
- ✅ Submit KPIs for approval
- ✅ Approve/Reject KPIs
- ✅ Delete draft KPIs
- ✅ Filter KPIs by year/quarter/status
- ✅ Search KPIs
- ✅ View KPI details
- ✅ Manage users (Phase 6)
- ✅ Manage system settings (Phase 6)

### Testing the Workflow

**1. Create a KPI:**
- Click "Create New KPI" on dashboard
- Fill in details (title, year, quarter)
- Optional: Select a template
- Set target and current values
- Adjust progress slider
- Click "Create KPI"

**2. Submit for Approval:**
- Go to KPI detail page
- Click "Submit for Approval"
- Status changes to "Submitted"

**3. Approve KPI:**
- As manager/admin, go to "Approvals" page
- Or view KPI detail page
- Click "Approve" (optionally add comment)
- Status changes to "Approved"

**4. View Statistics:**
- Dashboard shows real-time stats
- Total KPIs, Pending, Approved counts
- Average progress percentage

---

## 📁 Project Structure

```
bsv-okr-kpi/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── crud/        # Database operations
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   └── utils/       # Utilities
│   ├── scripts/         # CLI scripts
│   └── alembic/         # Database migrations
├── frontend/            # React application
│   └── src/
│       ├── components/  # Reusable components
│       ├── pages/       # Page components
│       ├── services/    # API clients
│       └── contexts/    # State management
├── data/                # Application data
│   ├── database/        # SQLite database
│   ├── uploads/         # File uploads (Phase 3)
│   ├── backups/         # Database backups
│   └── logs/            # Application logs
└── docs/                # Documentation
```

---

## 🔑 Default Credentials

**Admin Account:**
- Email: `admin@company.com`
- Password: `Admin123!`

**⚠️ IMPORTANT**: Change the password after first login!

---

## 🧪 Testing Checklist

- [ ] Login works
- [ ] Dashboard shows statistics
- [ ] Create KPI works
- [ ] Edit KPI works
- [ ] Delete draft KPI works
- [ ] Submit KPI works
- [ ] Approve KPI works (as manager/admin)
- [ ] Filters work (year, quarter, status)
- [ ] Search works
- [ ] Pagination works
- [ ] Logout works

---

## 📖 Documentation

- **Phase 1 Complete**: `PHASE1_COMPLETE.md`
- **Phase 2 Complete**: `PHASE2_COMPLETE.md`
- **Full Review**: `PHASE1_AND_2_REVIEW.md`
- **API Reference**: `docs/API.md`
- **Architecture**: `docs/ARCHITECTURE.md`
- **Database**: `docs/DATABASE.md`
- **Deployment**: `docs/DEPLOYMENT.md`

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt

# Check .env file exists
ls -la .env

# Check SECRET_KEY is set
cat .env | grep SECRET_KEY
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check .env file exists
ls -la .env
```

### Database errors
```bash
# Reset database
rm -rf data/database/*
alembic upgrade head

# Recreate admin
python scripts/create_admin.py \
  --email admin@company.com \
  --password Admin123! \
  --fullname "System Admin"
```

### Login fails
- Check credentials match what you set
- Check backend is running (http://localhost:8000/health)
- Check browser console for errors
- Check backend logs

---

## 🚢 Deployment

### Using Docker (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access**:
- Frontend: http://localhost
- Backend: http://localhost/api
- API Docs: http://localhost/api/docs

### Manual Deployment

See `docs/DEPLOYMENT.md` for detailed instructions for:
- Traditional VPS
- Docker
- Cloud platforms (AWS, Azure, GCP)
- Kubernetes

---

## 🔐 Security Notes

### Before Production:
1. ✅ Change default admin password
2. ✅ Generate strong SECRET_KEY
3. ✅ Set ENVIRONMENT=production
4. ✅ Enable HTTPS
5. ✅ Configure CORS_ORIGINS
6. ✅ Set up firewall
7. ✅ Enable database backups
8. ✅ Set up monitoring

### Environment Variables:
```bash
# Backend (.env)
SECRET_KEY=<your-secret-key>
ENVIRONMENT=production
DATABASE_URL=sqlite:////data/database/kpi.db
CORS_ORIGINS=["https://yourdomain.com"]

# Frontend (.env)
VITE_API_URL=https://api.yourdomain.com/api/v1
```

---

## 📈 Next Steps

### Phase 3: File Management (Optional)
- Upload evidence files
- File preview
- Download files

### Phase 4: Collaboration (Optional)
- Comments on KPIs
- Email notifications
- Activity timeline

### Phase 5: Reporting (Optional)
- PDF reports
- Excel exports
- Analytics dashboard

---

## 💬 Support

### Questions?
1. Check documentation in `docs/`
2. Review phase completion files
3. Run verification scripts:
   - `./verify_phase1.sh`
   - `./verify_phase2.sh`

### Found a Bug?
1. Check logs in `data/logs/`
2. Check browser console
3. Check backend terminal

---

## 🎉 You're Ready!

Your KPI Management System is now running with:
- ✅ Complete authentication system
- ✅ Role-based access control
- ✅ Full KPI management
- ✅ Approval workflows
- ✅ Beautiful responsive UI

**Enjoy using your KPI Management System!** 🚀
