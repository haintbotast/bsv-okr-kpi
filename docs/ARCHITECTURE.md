# Kiến Trúc Hệ Thống - Hệ Thống Quản Lý KPI

**Phiên bản**: 1.0.0
**Quy mô mục tiêu**: ~30 người dùng
**Triết lý thiết kế**: Keep It Simple - Đơn giản, dễ bảo trì, tiết kiệm chi phí

---

## 📋 Tổng Quan Dự Án

### Mục Đích

Xây dựng Hệ Thống Quản Lý KPI (Key Performance Indicator) hoàn chỉnh, sẵn sàng cho production, được tối ưu hóa cho đội ngũ nhỏ (~30 người dùng). Hệ thống phải:

- ✓ **Tự chứa** (SQLite database, local file storage)
- ✓ **Dễ triển khai** (Docker Compose, chỉ 2 containers)
- ✓ **Tiết kiệm chi phí** (không cần dịch vụ bên ngoài)
- ✓ **Bảo mật** (JWT auth, bcrypt passwords, RBAC)
- ✓ **Thân thiện người dùng** (giao diện hiện đại, responsive design)
- ✓ **Dễ bảo trì** (code sạch, có tài liệu, có tests)

### Người Dùng Mục Tiêu

**Phân bổ người dùng (~30 users):**
- **Phòng IT**: 5-10 người
- **Ban Quản Lý**: 3-5 người
- **Nhân Viên Phòng Ban**: 15-20 người

**Vai trò người dùng:**

1. **Admin** (Quản trị viên)
   - Toàn quyền truy cập hệ thống
   - Quản lý người dùng và templates
   - Cấu hình hệ thống
   - Xem tất cả KPIs

2. **Manager** (Quản lý)
   - Phê duyệt/từ chối KPIs của đội
   - Xem KPIs của đội
   - Tạo KPIs của riêng mình
   - Tạo báo cáo đội

3. **Employee** (Nhân viên)
   - Tạo KPIs của riêng mình
   - Gửi để phê duyệt
   - Upload minh chứng
   - Tạo báo cáo cá nhân

### Yêu Cầu Nghiệp Vụ

**Tính năng cốt lõi:**
1. **Quản lý KPIs theo quý** (Q1-Q4) mỗi năm
2. **Theo dõi tiến độ** với upload minh chứng
3. **Hỗ trợ workflow phê duyệt** (Gửi → Xem xét → Phê duyệt/Từ chối)
4. **Tạo báo cáo** (xuất PDF/Excel)
5. **Kiểm soát truy cập dựa trên vai trò** (Admin, Manager, Employee)
6. **Bình luận và cộng tác**

**Phân loại KPI:**
- **Mission** (Nhiệm vụ): Mục tiêu chiến lược dài hạn
- **Goal** (Mục tiêu): Các mục tiêu cụ thể có thể đo lường
- **Task** (Công việc): Các hạng mục công việc thực thi

**Phương thức đo lường:**
- **Percentage** (Phần trăm) - ví dụ: 99.9% uptime
- **Number** (Số lượng) - ví dụ: 100 đơn hàng
- **Boolean** (Có/Không) - ví dụ: hoàn thành/chưa hoàn thành

---

## 🏗️ Quyết Định Kiến Trúc

### Tại Sao SQLite Thay Vì PostgreSQL?

✅ **Lý do chọn SQLite:**
- Single file database - dễ backup
- Không cần DB server riêng
- ACID compliant (đảm bảo tính toàn vẹn dữ liệu)
- Hiệu suất tốt cho <100 users
- Zero configuration

⚠️ **Giới hạn**:
- Concurrent writes hạn chế (giải quyết bằng WAL mode)
- Không thích hợp cho distributed systems

### Tại Sao Local Storage Thay Vì S3/MinIO?

✅ **Lý do chọn Local Storage:**
- Không cần dịch vụ ngoài
- Truy cập nhanh qua filesystem
- Nginx serves files hiệu quả
- Zero cost

⚠️ **Giới hạn**:
- Scaling ngang khó hơn (ổn với 30 users)

### Tại Sao APScheduler Thay Vì Celery?

✅ **Lý do chọn APScheduler:**
- In-process scheduler - không cần message broker
- Đủ cho backup/cleanup/email
- Zero dependencies bổ sung
- Simple configuration

⚠️ **Giới hạn**:
- Không phù hợp cho distributed tasks

---

## 📐 Sơ Đồ Kiến Trúc

### Kiến Trúc Tổng Thể

```
┌─────────────────────────────────────────────────────┐
│             Người Dùng (Browsers/Mobile)            │
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

### Luồng Request

1. **User Request** → Nginx (Port 80/443)
2. **Static Assets** → Nginx serves React build
3. **API Calls** → Nginx proxies to FastAPI (Port 8000)
4. **File Uploads** → FastAPI → Local filesystem
5. **Database** → FastAPI → SQLite (WAL mode)

---

## 🛠️ Stack Công Nghệ

### Backend

**Framework & Core:**
- Language: Python 3.11+
- Framework: FastAPI 0.108+
- ORM: SQLAlchemy 2.0+
- Database: SQLite3
- Migration: Alembic

**Authentication & Security:**
- JWT: python-jose
- Password Hashing: passlib[bcrypt]
- CORS: fastapi-cors-middleware

**Background Jobs:**
- Scheduler: APScheduler 3.10+

**File & Export:**
- File Handling: python-multipart
- PDF Generation: reportlab
- Excel Export: openpyxl
- Word Generation: python-docx

**Testing:**
- pytest
- pytest-cov
- httpx (async testing)

### Frontend

**Framework & Build:**
- Framework: React 18+
- Build Tool: Vite 5+
- Language: JavaScript (hoặc TypeScript)

**Styling & UI:**
- CSS Framework: Tailwind CSS 3+
- UI Components: shadcn/ui (tùy chọn)

**State & Data:**
- State Management: React Context + hooks
- HTTP Client: Axios
- Forms: React Hook Form

**Routing & Navigation:**
- Router: React Router v6

**Charts & Visualization:**
- Charts: Recharts hoặc Chart.js
- Date Handling: date-fns
- File Preview: react-pdf, react-file-viewer

### Deployment

**Containerization:**
- Docker + Docker Compose

**Web Server:**
- Nginx (reverse proxy + static files)

**Process Manager:**
- Uvicorn (cho FastAPI)

---

## 🗄️ Database Schema (8 Bảng)

### Quan Hệ Giữa Các Bảng

```
users (1) ──────────< (N) kpis
  │                      │
  │                      ├──────────< (N) kpi_evidence
  │                      ├──────────< (N) kpi_comments
  │                      └──────────< (N) kpi_history
  │
  ├──────────< (N) notifications
  └──────────< (N) kpi_templates

kpis (N) ────────> (1) kpi_templates [optional]
kpis (N) ────────> (1) users [approved_by]
```

### Danh Sách Bảng

1. **users** - Người dùng và phân quyền
2. **kpi_templates** - Templates KPI có sẵn
3. **kpis** - KPIs chính (bảng trung tâm)
4. **kpi_evidence** - Files minh chứng
5. **kpi_comments** - Bình luận và thảo luận
6. **kpi_history** - Lịch sử thay đổi (audit trail)
7. **notifications** - Thông báo cho người dùng
8. **system_settings** - Cài đặt hệ thống

Chi tiết schema xem: [DATABASE.md](./DATABASE.md)

---

## 🔒 Bảo Mật

### Authentication (Xác Thực)

- **JWT tokens** (8h access + 7d refresh)
- **bcrypt** password hashing (cost 12+)
- **Session timeout**: 8 giờ
- **Token refresh** mechanism

### Authorization (Phân Quyền)

- **RBAC** (Role-Based Access Control)
- **3 vai trò**: Admin, Manager, Employee
- **Permission checks** ở mọi API endpoint
- **Resource ownership validation**

### File Security

- **Whitelist** file types
- **Max size**: 50MB per file
- **Filename sanitization** (UUID naming)
- **Storage** ngoài web root
- **Nginx** serves với security headers

### API Security

- **CORS whitelist** (không dùng wildcards)
- **Input validation** (Pydantic schemas)
- **Parameterized queries** (SQLAlchemy ORM)
- **XSS protection** (React auto-escaping)
- **Rate limiting** (optional)

Chi tiết xem: [SECURITY.md](./SECURITY.md)

---

## ⚡ Performance & Optimization

### Database Optimization

**WAL Mode:**
```sql
PRAGMA journal_mode=WAL;  -- Better concurrency
PRAGMA synchronous=NORMAL;  -- Balance speed/safety
PRAGMA cache_size=10000;  -- 40MB cache
```

**Indexing:**
- Indexes trên các cột thường query
- Composite indexes cho filters phổ biến
- Xem chi tiết trong DATABASE.md

**Pagination:**
- Default: 20 items per page
- Max: 100 items per page

### Frontend Optimization

**Build Optimization:**
- Code splitting
- Lazy loading components
- Tree shaking

**Asset Optimization:**
- Image compression
- Gzip compression (Nginx)
- Browser caching

**Runtime Optimization:**
- React.memo cho expensive components
- useMemo/useCallback hooks
- Virtual scrolling cho long lists

---

## 📈 Khả Năng Mở Rộng (Scalability)

### Quy Mô Hiện Tại (30 users)

**Server Requirements:**
- CPU: 2 cores
- RAM: 2GB
- Disk: 20GB SSD
- Network: 10 Mbps

**Expected Load:**
- Concurrent users: 10-15
- Requests/second: <50
- Database size: 500MB (year 1)

### Scaling Path

**50-100 users:**
- ✅ Tăng resources (4 cores, 4GB RAM)
- ✅ Giữ SQLite (vẫn đủ)
- ✅ Optimize queries
- ✅ Add caching layer (optional)

**>100 users:**
- 🔄 Migrate sang PostgreSQL
- 🔄 Add Redis cache
- 🔄 Horizontal scaling (multiple backends)
- 🔄 Load balancer

---

## 🚀 Deployment Strategy

### Development

```bash
docker-compose up -d
```

**Containers:**
- backend:8000
- frontend:3000 (dev server)

### Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Containers:**
- backend:8000 (internal only)
- frontend:80/443 (Nginx)

**Features:**
- Resource limits
- Health checks
- Auto-restart
- Log rotation
- SSL/TLS

Chi tiết xem: [DEPLOYMENT.md](./DEPLOYMENT.md)

---

## 🔄 Dự Phòng & Sao Lưu

### Automated Backups

**APScheduler job:**
- **Frequency**: Daily at 2 AM
- **Retention**: 30 days
- **Location**: `/data/backups/`
- **Format**: Compressed SQLite + uploads tar

### Manual Backup

```bash
docker-compose exec backend python scripts/backup.py
```

### Restore

```bash
docker-compose down
cp data/backups/kpi_YYYYMMDD.db data/database/kpi.db
docker-compose up -d
```

---

## 📊 So Sánh Chi Phí

### DIY Solution (Hệ Thống Này)

| Hạng mục | Chi phí | Ghi chú |
|----------|---------|---------|
| VPS Server (2GB RAM, 2 CPU) | $12/tháng | DigitalOcean, Linode, Hetzner |
| Tên miền (Domain) | $10/năm | Namecheap, Cloudflare |
| SSL Certificate | Miễn phí | Let's Encrypt |
| **Tổng cộng** | **~$154/năm** | Không giới hạn người dùng |

### SaaS Alternatives (30 người)

| Dịch vụ | Giá/User/Tháng | Chi phí năm (30 users) |
|---------|----------------|------------------------|
| Perdoo | $8 | $2,880 |
| Weekdone | $7 | $2,520 |
| Quantive | $10 | $3,600 |

**💰 Tiết kiệm: $2,366 - $3,446 mỗi năm (94-96% rẻ hơn!)**

**ROI:**
- Phát triển: 6-8 tuần (với Claude Code)
- Break-even: < 3 tháng
- Tiết kiệm liên tục: Hàng năm

---

## 📚 Tài Liệu Liên Quan

- [DATABASE.md](./DATABASE.md) - Chi tiết schema database
- [SECURITY.md](./SECURITY.md) - Best practices bảo mật
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Hướng dẫn triển khai
- [MAINTENANCE.md](./MAINTENANCE.md) - Bảo trì hệ thống
- [API.md](./API.md) - Tài liệu API (Vietnamese)
- [../docs/technical/API_REFERENCE.md](./technical/API_REFERENCE.md) - API Reference (English)

---

## 🎯 Metrics Thành Công

### Technical Metrics

- ✅ System uptime: >99%
- ✅ Page load time: <3 seconds
- ✅ API response time: <500ms
- ✅ Database size: <500MB (first year)
- ✅ Zero data loss
- ✅ Zero security breaches

### Business Metrics

- ✅ User adoption: 100% of target users
- ✅ KPI completion rate: >80% on time
- ✅ User satisfaction: >4/5 rating
- ✅ Support tickets: <10 per month
- ✅ Training time: <2 hours per user

---

**Tài liệu này được cập nhật**: 2025-10-31
**Phiên bản**: 1.0.0
