# Kiến Trúc Hệ Thống - Hệ Thống Quản Lý KPI

**Phiên bản**: 1.0.0
**Quy mô**: ~30 người dùng
**Triết lý**: Keep It Simple - Đơn giản, dễ bảo trì, tiết kiệm chi phí

---

## Quyết Định Kiến Trúc Quan Trọng

### Tại Sao SQLite Thay Vì PostgreSQL?
✅ Single file database - dễ backup
✅ Không cần DB server riêng
✅ ACID compliant
✅ Hiệu suất tốt cho <100 users
⚠️ Giới hạn: Concurrent writes hạn chế (dùng WAL mode)

### Tại Sao Local Storage Thay Vì S3?
✅ Không cần dịch vụ ngoài
✅ Truy cập nhanh qua filesystem
✅ Nginx serves files hiệu quả
⚠️ Giới hạn: Scaling ngang khó hơn

### Tại Sao APScheduler Thay Vì Celery?
✅ In-process scheduler - không cần message broker
✅ Đủ cho backup/cleanup/email
✅ Zero dependencies bổ sung

---

## Sơ Đồ Kiến Trúc

```
Người dùng (Browser) → Nginx (80/443)
    ↓                     ↓
Frontend (React)    Backend (FastAPI:8000)
                          ↓
              SQLite + Uploads + Backups
```

---

## Stack Công Nghệ

**Backend**: FastAPI + SQLAlchemy + SQLite + JWT + APScheduler
**Frontend**: React 18 + Vite + Tailwind CSS + Axios
**Deployment**: Docker Compose (2 containers)
**Web Server**: Nginx

---

## Database Schema (8 Bảng)

1. users - Người dùng
2. kpi_templates - Templates
3. kpis - KPIs chính
4. kpi_evidence - Files minh chứng
5. kpi_comments - Bình luận
6. kpi_history - Lịch sử
7. notifications - Thông báo
8. system_settings - Cài đặt

Chi tiết xem [03_DATABASE_SCHEMA.md](./03_DATABASE_SCHEMA.md)

---

## Security

- JWT tokens (8h access + 7d refresh)
- bcrypt password hashing (cost 12+)
- RBAC (Admin, Manager, Employee)
- File upload validation
- CORS whitelist

---

## Performance

**Tối ưu database**:
- WAL mode cho concurrency
- Indexes trên các cột thường query
- Pagination (default 20 items)

**Tối ưu frontend**:
- Code splitting & lazy loading
- Asset compression
- Memoization

---

## Scalability Plan

**30 users (hiện tại)**: SQLite + 2GB RAM + 2 CPU cores
**50-100 users**: Tăng resources, giữ SQLite
**>100 users**: Migrate sang PostgreSQL + Redis

---

**Chi tiết**: Xem file gốc cho specification đầy đủ
