# 🚀 Hướng Dẫn Bắt Đầu - Hệ Thống Quản Lý KPI

> **Hệ thống quản lý KPI nhẹ, tự lưu trữ**
> Tối ưu cho ~30 người dùng | SQLite3 | Docker | Tiết kiệm chi phí (~$154/năm so với $2,500+/năm cho SaaS)

---

## 📦 Nội Dung Package

Package này bao gồm mọi thứ bạn cần để xây dựng và triển khai Hệ Thống Quản Lý KPI sẵn sàng cho production:

1. **`docs/technical/SPECIFICATION.txt`** - Đặc tả đầy đủ và hướng dẫn cho Claude Code
2. **`GETTING_STARTED.md`** (file này) - Hướng dẫn từng bước
3. **`deployment/docker-compose.yml`** - Cấu hình Docker triển khai sẵn sàng
4. **`backend/.env.example`** - Template biến môi trường với tất cả settings
5. **`docs/`** - Tài liệu đầy đủ

---

## 🎯 Quick Start (3 Bước)

### Bước 1: Chuẩn Bị Dự Án

```bash
# Tạo thư mục dự án (nếu chưa có)
cd bsv-okr-kpi

# Sao chép file .env
cp backend/.env.example backend/.env

# QUAN TRỌNG: Chỉnh sửa backend/.env và cập nhật các giá trị:
# - SECRET_KEY (tạo với: openssl rand -hex 32)
# - CORS_ORIGINS (thêm domain của bạn)
# - ADMIN_EMAIL và ADMIN_PASSWORD
```

### Bước 2: Xây Dựng với Claude Code

```bash
# Khởi động Claude Code trong thư mục dự án
claude-code

# Trong Claude Code, dán toàn bộ nội dung docs/technical/SPECIFICATION.txt
# Sau đó nói: "Build this system starting with Phase 1"

# Claude Code sẽ tạo tất cả code!
```

### Bước 3: Triển Khai

```bash
# Khởi động ứng dụng (development)
docker-compose -f deployment/docker-compose.yml up -d

# Khởi tạo database
docker-compose -f deployment/docker-compose.yml exec backend python scripts/init_db.py

# Tạo admin user
docker-compose -f deployment/docker-compose.yml exec backend python scripts/create_admin.py \
  --email admin@company.com \
  --password "SecurePassword123!" \
  --fullname "System Admin"

# Truy cập ứng dụng của bạn
# http://localhost (hoặc IP server của bạn)
```

---

## 🎯 Tổng Quan Hệ Thống

### Tính Năng Chính

- ✅ **Quản Lý Người Dùng** - Admin, Manager, Employee roles với RBAC
- ✅ **Theo Dõi KPI** - Tạo, theo dõi và quản lý KPIs theo quý (Q1-Q4)
- ✅ **Quản Lý Files** - Upload minh chứng (PDF, Office docs, images)
- ✅ **Approval Workflow** - Gửi → Xem xét → Phê duyệt/Từ chối
- ✅ **Báo Cáo** - Tạo báo cáo PDF/Excel
- ✅ **Dashboard** - Phân tích trực quan và theo dõi tiến độ
- ✅ **Bình Luận** - Cộng tác trên KPIs
- ✅ **Thông Báo** - Hệ thống thông báo trong ứng dụng
- ✅ **Audit Log** - Theo dõi tất cả hoạt động
- ✅ **Sao Lưu Tự Động** - Backup database hàng ngày

### Stack Công Nghệ

**Backend:**
- FastAPI (Python 3.11+)
- SQLAlchemy ORM
- SQLite3 Database
- JWT Authentication
- APScheduler cho background jobs

**Frontend:**
- React 18+
- Tailwind CSS
- Vite build tool
- Axios cho API calls
- React Router cho navigation

**Deployment:**
- Docker & Docker Compose
- Nginx reverse proxy
- Local file storage
- Triển khai single server

### Kiến Trúc

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

---

## 📖 Workflow Phát Triển với Claude Code

### 1. Phát Triển Lặp (Iterative Development)

```
BẠN: "Implement user authentication with JWT"
CLAUDE CODE: [Tạo code authentication]
BẠN: "Test the login endpoint"
CLAUDE CODE: [Tạo test]
BẠN: "Fix the token refresh logic"
CLAUDE CODE: [Cập nhật code]
```

### 2. Pattern Yêu Cầu Tính Năng

```
BẠN: "Add file upload feature with these requirements:
- Support PDF, DOCX, XLSX
- Max 50MB per file
- Store in /data/uploads
- Preview in browser"

CLAUDE CODE: [Implements complete feature]
```

### 3. Pattern Sửa Lỗi

```
BẠN: "Fix bug: Users can see other users' KPIs
Error appears in kpi_list view"

CLAUDE CODE: [Analyzes and fixes]
```

### 4. Pattern Code Review

```
BẠN: "Review the KPI approval workflow code for security issues"

CLAUDE CODE: [Reviews and suggests improvements]
```

---

## 🛠️ Lệnh Thông Dụng

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
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Docker Deployment

```bash
# Khởi động services (development)
docker-compose -f deployment/docker-compose.yml up -d

# Khởi động services (production)
docker-compose -f deployment/docker-compose.prod.yml up -d

# Xem logs
docker-compose -f deployment/docker-compose.yml logs -f
docker-compose -f deployment/docker-compose.yml logs -f backend
docker-compose -f deployment/docker-compose.yml logs -f frontend

# Dừng services
docker-compose -f deployment/docker-compose.yml down

# Rebuild sau khi thay đổi code
docker-compose -f deployment/docker-compose.yml up -d --build

# Thực thi lệnh trong containers
docker-compose -f deployment/docker-compose.yml exec backend bash
docker-compose -f deployment/docker-compose.yml exec backend python scripts/backup.py
```

### Quản Lý Database

```bash
# Khởi tạo database (lần đầu)
docker-compose -f deployment/docker-compose.yml exec backend python scripts/init_db.py

# Tạo admin user
docker-compose -f deployment/docker-compose.yml exec backend python scripts/create_admin.py

# Backup database
docker-compose -f deployment/docker-compose.yml exec backend python scripts/backup.py
# Hoặc thủ công:
cp data/database/kpi.db data/backups/kpi_$(date +%Y%m%d).db

# Restore database
docker-compose -f deployment/docker-compose.yml down
cp data/backups/kpi_YYYYMMDD.db data/database/kpi.db
docker-compose -f deployment/docker-compose.yml up -d

# Chạy migrations
docker-compose -f deployment/docker-compose.yml exec backend alembic upgrade head
```

---

## 🔒 Security Checklist

Trước khi triển khai lên production:

- [ ] Thay đổi `SECRET_KEY` trong `backend/.env` (dùng `openssl rand -hex 32`)
- [ ] Cập nhật `ADMIN_PASSWORD` với mật khẩu mạnh
- [ ] Cấu hình `CORS_ORIGINS` với domain thực tế của bạn
- [ ] Thiết lập HTTPS với Let's Encrypt
- [ ] Xem xét giới hạn file upload
- [ ] Bật automated backups
- [ ] Thiết lập log rotation
- [ ] Cấu hình firewall rules
- [ ] Thay đổi default ports (tùy chọn)
- [ ] Thiết lập monitoring (tùy chọn)

---

## 📊 So Sánh Chi Phí

### Giải Pháp DIY (Hệ Thống Này)

| Hạng mục | Chi phí | Ghi chú |
|----------|---------|---------|
| VPS Server (2GB RAM, 2 CPU) | $12/tháng | DigitalOcean, Linode, Hetzner |
| Domain | $10/năm | Namecheap, Cloudflare |
| SSL Certificate | Miễn phí | Let's Encrypt |
| **Tổng** | **~$154/năm** | Cho không giới hạn users |

### SaaS Alternatives (30 users)

| Dịch vụ | Giá/User/Tháng | Chi phí năm (30 users) |
|---------|----------------|------------------------|
| Perdoo | $8 | $2,880 |
| Weekdone | $7 | $2,520 |
| Quantive | $10 | $3,600 |

**💰 Tiết kiệm: $2,366 - $3,446 mỗi năm (94-96% rẻ hơn!)**

**ROI:**
- Phát triển: 6-8 tuần (với Claude Code)
- Break-even: < 3 tháng
- Tiết kiệm liên tục: Miễn phí (chỉ trả server costs)

---

## 🎯 Khả Năng Hệ Thống

Tối ưu cho:
- ✅ **30 users** (có thể scale lên 100+ nếu cần)
- ✅ **5,000-10,000 KPIs** mỗi năm
- ✅ **50,000+ file uploads** (tối đa 50MB mỗi file)
- ✅ **100,000+ comments/notifications**

Ước tính kích thước database:
- Năm 1: ~500 MB
- Năm 2: ~1 GB
- Năm 3: ~1.5 GB

Server resources:
- **CPU**: 2 cores (đủ)
- **RAM**: 2GB (thoải mái)
- **Disk**: 20GB SSD (dư giả)
- **Network**: 10 Mbps

---

## 📱 Vai Trò & Quyền Người Dùng

### Admin
- Toàn quyền truy cập hệ thống
- Quản lý users
- Quản lý templates
- System settings
- Xem tất cả KPIs
- Tạo reports

### Manager
- Phê duyệt/từ chối KPIs của đội
- Xem KPIs của đội
- Tạo KPIs riêng
- Tạo team reports
- Thêm comments

### Employee
- Tạo KPIs riêng
- Gửi để phê duyệt
- Upload minh chứng
- Thêm comments
- Xem dashboard riêng
- Tạo reports riêng

---

## 🐛 Troubleshooting

### Issue: Không thể start containers

```bash
# Kiểm tra xem ports có đang được sử dụng không
sudo lsof -i :80
sudo lsof -i :8000

# Kiểm tra Docker service
sudo systemctl status docker

# Xem container logs
docker-compose -f deployment/docker-compose.yml logs
```

### Issue: Database locked

```bash
# Enable WAL mode (tốt hơn cho concurrency)
docker-compose -f deployment/docker-compose.yml exec backend python -c "
import sqlite3
conn = sqlite3.connect('/data/database/kpi.db')
conn.execute('PRAGMA journal_mode=WAL')
conn.close()
"
```

### Issue: File upload fails

```bash
# Kiểm tra permissions
docker-compose -f deployment/docker-compose.yml exec backend ls -la /data/uploads

# Fix permissions
docker-compose -f deployment/docker-compose.yml exec backend chmod 777 /data/uploads
```

### Issue: Frontend không reach được backend

```bash
# Kiểm tra CORS settings trong backend/.env
# Verify backend đang chạy
curl http://localhost:8000/health

# Kiểm tra Docker network
docker network inspect kpi-system_kpi-network
```

---

## 📚 Tài Liệu

Sau khi xây dựng với Claude Code, bạn sẽ có:

1. **API Documentation** - Swagger UI tự động tại `/docs`
2. **User Guide** - Trợ giúp và tooltips trong app
3. **Admin Guide** - Tài liệu quản trị hệ thống
4. **Technical Docs** - Code comments và README files

Truy cập API docs:
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

### Manual Testing Checklist

- [ ] User có thể register/login
- [ ] User có thể tạo KPI
- [ ] User có thể upload files
- [ ] Manager có thể approve/reject
- [ ] Reports generate đúng
- [ ] Dashboard hiển thị data
- [ ] Comments hoạt động
- [ ] Notifications xuất hiện
- [ ] Mobile responsive
- [ ] Hoạt động trên Chrome, Firefox, Safari

---

## 🚀 Triển Khai Lên Production

Xem hướng dẫn chi tiết: [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)

### Các Bước Tóm Tắt

1. **Server Setup** - Update system, install Docker
2. **SSL Setup** - Let's Encrypt certificate
3. **Deploy Application** - Docker Compose production
4. **Initialize Database** - Run init scripts
5. **Setup Backups** - Automated cron job

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:

1. **Check Documentation**: Xem lại docs/
2. **View Logs**: Check Docker logs hoặc application logs
3. **Search Issues**: Google error messages
4. **Simplify**: Chia nhỏ vấn đề, test từng phần

---

## ⏱️ Timeline Ước Tính

| Phase | Tasks | Thời gian | Trạng thái |
|-------|-------|-----------|-----------|
| Phase 1 | Core Infrastructure | 1 tuần | ⏳ |
| Phase 2 | KPI Management | 1 tuần | ⏳ |
| Phase 3 | File Management | 1 tuần | ⏳ |
| Phase 4 | Workflow & Collaboration | 1 tuần | ⏳ |
| Phase 5 | Reporting & Analytics | 1 tuần | ⏳ |
| Phase 6 | Admin Features | 1 tuần | ⏳ |
| Phase 7 | Optimization & Polish | 2 tuần | ⏳ |
| **Tổng** | | **8 tuần** | |

---

## 🎯 Checklist Hoàn Thành

Hệ thống hoàn thành khi:

- [ ] User có thể login/logout
- [ ] User có thể tạo, sửa, xóa KPI
- [ ] User có thể upload evidence files
- [ ] Manager có thể approve/reject KPIs
- [ ] System generate reports (PDF/Excel)
- [ ] Dashboard hiển thị statistics
- [ ] Comment system hoạt động
- [ ] Notifications hiển thị
- [ ] Responsive trên mobile
- [ ] Docker deployment hoạt động
- [ ] Database backup tự động
- [ ] Documentation đầy đủ
- [ ] Tests pass > 70%

---

## 🚀 Next Steps

1. **Đọc kỹ specification** (`docs/technical/SPECIFICATION.txt`)
2. **Setup môi trường development**
3. **Khởi động Claude Code**
4. **Bắt đầu Phase 1**
5. **Test và iterate**
6. **Deploy to production**
7. **Train users**
8. **Collect feedback**
9. **Plan improvements**

---

## 📖 Tài Liệu Liên Quan

- [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) - Kiến trúc hệ thống
- [docs/DATABASE.md](./docs/DATABASE.md) - Schema database
- [docs/SECURITY.md](./docs/SECURITY.md) - Best practices bảo mật
- [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) - Hướng dẫn triển khai
- [docs/MAINTENANCE.md](./docs/MAINTENANCE.md) - Bảo trì & troubleshooting
- [docs/API.md](./docs/API.md) - Tài liệu API (Vietnamese)
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Hướng dẫn đóng góp

---

**Chúc bạn code vui vẻ!** 🎉

Remember: Keep it simple, test thoroughly, and focus on your 30 users' needs!
