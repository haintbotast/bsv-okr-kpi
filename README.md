# 🎯 Hệ Thống Quản Lý KPI

> **Hệ thống tự lưu trữ, nhẹ, tiết kiệm chi phí**
> Tối ưu cho ~30 người dùng | SQLite3 | Docker | Chi phí ~$154/năm (so với $2,500+/năm cho SaaS)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18+](https://img.shields.io/badge/react-18+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.108+-009688.svg)](https://fastapi.tiangolo.com/)

---

## 📋 Tổng Quan

Hệ Thống Quản Lý KPI (Key Performance Indicator) hoàn chỉnh, sẵn sàng cho production, được tối ưu hóa cho các đội nhỏ (~30 người dùng). Hệ thống tự chứa (SQLite, local storage), dễ triển khai (Docker Compose), và cực kỳ tiết kiệm chi phí.

### ✨ Tính Năng Chính

- 🔐 **Xác thực & Phân quyền** - JWT auth, 3 vai trò (Admin, Manager, Employee)
- 📊 **Quản lý KPI** - Theo dõi theo quý (Q1-Q4), workflow phê duyệt
- 📁 **Quản lý Files** - Upload minh chứng (PDF, Office, images, max 50MB)
- 📈 **Báo cáo** - Tạo báo cáo PDF/Excel, analytics dashboard
- 💬 **Cộng tác** - Comments, notifications, activity timeline
- 🔄 **Backup tự động** - Sao lưu database hàng ngày
- 🎨 **UI hiện đại** - React + Tailwind CSS, responsive

### 🏗️ Stack Công Nghệ

**Backend:**
- FastAPI (Python 3.11+)
- SQLAlchemy ORM + SQLite3
- JWT Authentication
- APScheduler (background jobs)

**Frontend:**
- React 18+ + Vite
- Tailwind CSS
- Axios + React Router

**Deployment:**
- Docker + Docker Compose
- Nginx reverse proxy
- Single server deployment

---

## 🚀 Quick Start

### Yêu Cầu

- Docker & Docker Compose
- Git

### Cài Đặt

```bash
# 1. Clone repository
git clone https://github.com/haintbotast/bsv-okr-kpi.git
cd bsv-okr-kpi

# 2. Cấu hình môi trường
cp backend/.env.example backend/.env
# Chỉnh sửa backend/.env:
# - SECRET_KEY (tạo với: openssl rand -hex 32)
# - ADMIN_PASSWORD
# - CORS_ORIGINS

# 3. Khởi động services
docker-compose -f deployment/docker-compose.yml up -d

# 4. Khởi tạo database
docker-compose -f deployment/docker-compose.yml exec backend python scripts/init_db.py

# 5. Tạo admin user
docker-compose -f deployment/docker-compose.yml exec backend python scripts/create_admin.py \
  --email admin@company.com \
  --password "SecurePassword123!" \
  --fullname "System Admin"

# 6. Truy cập ứng dụng
# http://localhost
```

**Chi tiết**: Xem [GETTING_STARTED.md](./GETTING_STARTED.md)

---

## 📁 Cấu Trúc Dự Án

```
bsv-okr-kpi/
├── backend/               # FastAPI backend
│   ├── app/              # Application code
│   ├── scripts/          # Utility scripts
│   ├── tests/            # Backend tests
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── frontend/             # React frontend
│   ├── src/              # Source code
│   ├── public/           # Static assets
│   ├── Dockerfile
│   ├── package.json
│   └── README.md
│
├── deployment/           # Docker configs
│   ├── docker-compose.yml      # Development
│   ├── docker-compose.prod.yml # Production
│   └── nginx.prod.conf
│
├── docs/                 # Documentation (Vietnamese)
│   ├── ARCHITECTURE.md   # System architecture
│   ├── DATABASE.md       # Database schema
│   ├── SECURITY.md       # Security practices
│   ├── DEPLOYMENT.md     # Deployment guide
│   ├── MAINTENANCE.md    # Maintenance guide
│   ├── API.md            # API docs (Vietnamese)
│   └── technical/        # English technical specs
│       ├── API_REFERENCE.md
│       ├── DEVELOPMENT_PHASES.md
│       └── SPECIFICATION.txt
│
├── data/                 # Runtime data (gitignored)
│   ├── database/         # SQLite database
│   ├── uploads/          # Uploaded files
│   ├── backups/          # Database backups
│   └── logs/             # Application logs
│
├── scripts/              # Utility scripts
├── .github/              # GitHub Actions (optional)
├── GETTING_STARTED.md    # Quick start guide
├── CONTRIBUTING.md       # Contribution guidelines
├── CHANGELOG.md          # Version history
└── LICENSE               # MIT License
```

---

## 📖 Tài Liệu

### Bắt Đầu
- **[GETTING_STARTED.md](./GETTING_STARTED.md)** - Hướng dẫn nhanh, setup, workflow với Claude Code
- **[backend/README.md](./backend/README.md)** - Backend setup và development
- **[frontend/README.md](./frontend/README.md)** - Frontend setup và development

### Kỹ Thuật (Vietnamese)
- **[docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - Kiến trúc hệ thống, quyết định thiết kế
- **[docs/DATABASE.md](./docs/DATABASE.md)** - Schema database, queries
- **[docs/SECURITY.md](./docs/SECURITY.md)** - Best practices bảo mật
- **[docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)** - Hướng dẫn triển khai production
- **[docs/MAINTENANCE.md](./docs/MAINTENANCE.md)** - Bảo trì, troubleshooting
- **[docs/API.md](./docs/API.md)** - Tài liệu API (tiếng Việt)

### Kỹ Thuật (English)
- **[docs/technical/API_REFERENCE.md](./docs/technical/API_REFERENCE.md)** - Complete API reference
- **[docs/technical/DEVELOPMENT_PHASES.md](./docs/technical/DEVELOPMENT_PHASES.md)** - 7-phase development plan
- **[docs/technical/SPECIFICATION.txt](./docs/technical/SPECIFICATION.txt)** - Full system specification

### Contributing
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Guidelines cho contributors
- **[CHANGELOG.md](./CHANGELOG.md)** - Version history

---

## 🎯 Vai Trò Người Dùng

| Vai trò | Quyền hạn |
|---------|-----------|
| **Admin** | Toàn quyền: quản lý users, templates, settings, xem tất cả KPIs |
| **Manager** | Phê duyệt KPIs của đội, xem KPIs của đội, tạo KPIs riêng, báo cáo đội |
| **Employee** | Tạo KPIs riêng, gửi phê duyệt, upload minh chứng, báo cáo cá nhân |

---

## 💰 So Sánh Chi Phí

### DIY (Hệ thống này)
- **Server**: $12/tháng (2GB RAM, 2 CPU)
- **Domain**: $10/năm
- **SSL**: Miễn phí (Let's Encrypt)
- **Tổng**: **~$154/năm** (không giới hạn users)

### SaaS Alternatives (30 users)
- **Perdoo**: $2,880/năm
- **Weekdone**: $2,520/năm
- **Quantive**: $3,600/năm

**💰 Tiết kiệm: $2,366 - $3,446/năm (94-96% rẻ hơn!)**

---

## 🛠️ Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Testing

```bash
# Backend tests
cd backend
pytest --cov=app tests/

# Frontend tests (if configured)
cd frontend
npm test
```

---

## 🚀 Deployment

### Development

```bash
docker-compose -f deployment/docker-compose.yml up -d
```

### Production

```bash
docker-compose -f deployment/docker-compose.prod.yml up -d --build
```

**Chi tiết**: Xem [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)

---

## 🧪 Testing

- **Unit Tests**: pytest (backend), vitest (frontend - optional)
- **E2E Tests**: Playwright/Cypress (optional)
- **Manual Testing**: Checklist trong [docs/technical/DEVELOPMENT_PHASES.md](./docs/technical/DEVELOPMENT_PHASES.md)

**Target Coverage**: >70%

---

## 📊 Capacity

Hệ thống được thiết kế cho:
- ✅ 30 users (có thể scale lên 100+)
- ✅ 5,000-10,000 KPIs/năm
- ✅ 50,000+ file uploads (50MB max mỗi file)
- ✅ 100,000+ comments/notifications

**Server Requirements**:
- CPU: 2 cores
- RAM: 2GB
- Disk: 20GB SSD

---

## 🔒 Bảo Mật

- 🔐 JWT authentication (8h access + 7d refresh tokens)
- 🔑 bcrypt password hashing (cost 12+)
- 👥 RBAC (Role-Based Access Control)
- 📁 File upload validation (type + size)
- 🛡️ CORS whitelist configuration
- 🔒 HTTPS/SSL support (Let's Encrypt)

Xem chi tiết: [docs/SECURITY.md](./docs/SECURITY.md)

---

## 🤝 Contributing

Chúng tôi hoan nghênh contributions! Xem [CONTRIBUTING.md](./CONTRIBUTING.md) để biết:
- Coding standards
- Git workflow
- Testing requirements
- Pull request process

---

## 📝 License

MIT License - xem [LICENSE](./LICENSE) để biết chi tiết.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern Python web framework
- **React** - UI library
- **SQLite** - Lightweight database
- **Docker** - Containerization
- **Tailwind CSS** - Utility-first CSS framework

---

## 📞 Support & Contact

- **Documentation**: Xem thư mục `docs/`
- **Issues**: GitHub Issues (nếu sử dụng GitHub)
- **Email**: support@company.com (cập nhật email của bạn)

---

## 🗺️ Roadmap

### Version 1.0.0 (Current)
- ✅ Core KPI management
- ✅ File uploads
- ✅ Approval workflow
- ✅ Reports (PDF/Excel)
- ✅ Docker deployment

### Version 2.0.0 (Planned)
- 🔄 Real-time notifications (WebSocket)
- 🔄 Advanced analytics & BI
- 🔄 Mobile app (React Native)
- 🔄 Multi-language support
- 🔄 Dark mode

Xem chi tiết: [CHANGELOG.md](./CHANGELOG.md)

---

## ⭐ Star History

Nếu project này hữu ích, hãy cho một ⭐️!

---

**Built with ❤️ for IT teams managing ~30 users**

🚀 **Ready to start?** Xem [GETTING_STARTED.md](./GETTING_STARTED.md)
