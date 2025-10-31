# Backend - Hệ Thống Quản Lý KPI

FastAPI Backend cho Hệ Thống Quản Lý KPI.

---

## 🛠️ Stack Công Nghệ

- **Framework**: FastAPI 0.108+
- **Language**: Python 3.11+
- **ORM**: SQLAlchemy 2.0+
- **Database**: SQLite3
- **Migration**: Alembic
- **Authentication**: JWT (python-jose) + bcrypt
- **Background Jobs**: APScheduler
- **Testing**: pytest + pytest-cov

---

## 📦 Cài Đặt

### Yêu Cầu

- Python 3.11 hoặc cao hơn
- pip hoặc poetry

### Setup

```bash
# Tạo virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Cài đặt dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Chỉnh sửa .env với settings của bạn

# Khởi tạo database
python scripts/init_db.py

# Tạo admin user
python scripts/create_admin.py \
  --email admin@company.com \
  --password "SecurePassword123!" \
  --fullname "System Admin"

# Chạy server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🗂️ Cấu Trúc Thư Mục

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   │
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── kpi.py
│   │   └── ...
│   │
│   ├── schemas/             # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── kpi.py
│   │   └── ...
│   │
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencies (auth, db session)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── kpis.py
│   │       └── ...
│   │
│   ├── crud/                # CRUD operations
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── kpi.py
│   │   └── ...
│   │
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── email.py
│   │   ├── scheduler.py
│   │   └── ...
│   │
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── security.py
│       └── ...
│
├── alembic/                 # Database migrations
│   ├── env.py
│   └── versions/
│
├── scripts/                 # Utility scripts
│   ├── init_db.py          # Initialize database
│   ├── create_admin.py     # Create admin user
│   └── backup.py           # Backup database
│
├── tests/                   # Tests
│   ├── __init__.py
│   ├── conftest.py         # Test configuration
│   ├── test_auth.py
│   ├── test_kpis.py
│   └── ...
│
├── Dockerfile              # Docker image definition
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── alembic.ini            # Alembic configuration
├── pytest.ini             # Pytest configuration
└── README.md              # This file
```

---

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - Logout

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users` - List users (Admin/Manager)

### KPIs
- `GET /api/v1/kpis` - List KPIs (with filters)
- `POST /api/v1/kpis` - Create KPI
- `GET /api/v1/kpis/{id}` - Get KPI details
- `PUT /api/v1/kpis/{id}` - Update KPI
- `DELETE /api/v1/kpis/{id}` - Delete KPI
- `POST /api/v1/kpis/{id}/submit` - Submit for approval
- `POST /api/v1/kpis/{id}/approve` - Approve KPI (Manager)
- `POST /api/v1/kpis/{id}/reject` - Reject KPI (Manager)

### Files
- `POST /api/v1/files/upload` - Upload file
- `GET /api/v1/files/{id}` - Download file
- `DELETE /api/v1/files/{id}` - Delete file

### Reports
- `GET /api/v1/reports/pdf` - Generate PDF report
- `GET /api/v1/reports/excel` - Generate Excel report

**Full API documentation**: http://localhost:8000/docs

---

## 🗄️ Database

### Schema

8 bảng chính:
1. `users` - Người dùng và phân quyền
2. `kpi_templates` - Templates KPI
3. `kpis` - KPIs chính
4. `kpi_evidence` - Files minh chứng
5. `kpi_comments` - Bình luận
6. `kpi_history` - Lịch sử thay đổi
7. `notifications` - Thông báo
8. `system_settings` - Cài đặt hệ thống

Chi tiết: [../docs/DATABASE.md](../docs/DATABASE.md)

### Migrations

```bash
# Tạo migration mới
alembic revision --autogenerate -m "Add new column"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# View history
alembic history
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

---

## 🔒 Environment Variables

Xem `.env.example` để biết tất cả các biến có sẵn.

**Quan trọng:**
- `SECRET_KEY` - Generate với: `openssl rand -hex 32`
- `DATABASE_URL` - SQLite connection string
- `CORS_ORIGINS` - Allowed origins (comma-separated)

---

## 🐳 Docker

```bash
# Build image
docker build -t kpi-backend .

# Run container
docker run -d \
  --name kpi-backend \
  -p 8000:8000 \
  -v $(pwd)/data:/data \
  -e SECRET_KEY=your-secret-key \
  kpi-backend

# View logs
docker logs -f kpi-backend

# Stop container
docker stop kpi-backend
```

---

## 🔧 Development

### Code Style

```bash
# Format code
black app/

# Lint
flake8 app/

# Sort imports
isort app/

# Type checking
mypy app/
```

### Debug Mode

```bash
# Enable debug logs
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload
```

---

## 📚 Tài Liệu Liên Quan

- [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) - Kiến trúc hệ thống
- [../docs/DATABASE.md](../docs/DATABASE.md) - Schema database
- [../docs/SECURITY.md](../docs/SECURITY.md) - Best practices bảo mật
- [../docs/API.md](../docs/API.md) - Tài liệu API đầy đủ

---

## 🤝 Contributing

Xem [../CONTRIBUTING.md](../CONTRIBUTING.md) để biết hướng dẫn đóng góp.
