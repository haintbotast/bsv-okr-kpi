# Schema Cơ Sở Dữ Liệu - Hệ Thống Quản Lý KPI

**Database**: SQLite3
**Số bảng**: 8 bảng chính
**Relationships**: Foreign keys với CASCAD

E

---

## Sơ Đồ ERD

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

---

## 1. Bảng `users` - Người Dùng

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    role TEXT NOT NULL DEFAULT 'employee',
    department TEXT,
    position TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
```

**Vai trò (role)**:
- `admin` - Quản trị viên
- `manager` - Quản lý
- `employee` - Nhân viên

---

## 2. Bảng `kpi_templates` - Templates KPI

```sql
CREATE TABLE kpi_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    category TEXT,  -- mission, goal, task
    role TEXT,      -- admin, manager, employee
    measurement_method TEXT,
    target_type TEXT,  -- percentage, number, boolean
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_templates_category ON kpi_templates(category);
CREATE INDEX idx_templates_role ON kpi_templates(role);
```

**Categories**:
- `mission` - Nhiệm vụ
- `goal` - Mục tiêu
- `task` - Công việc

---

## 3. Bảng `kpis` - KPIs Chính

```sql
CREATE TABLE kpis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    template_id INTEGER,
    year INTEGER NOT NULL,
    quarter TEXT NOT NULL,  -- Q1, Q2, Q3, Q4
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    target_value TEXT,
    current_value TEXT,
    progress_percentage REAL,
    measurement_method TEXT,
    status TEXT DEFAULT 'draft',  -- draft, submitted, approved, rejected
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted_at TIMESTAMP,
    approved_at TIMESTAMP,
    approved_by INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (template_id) REFERENCES kpi_templates(id) ON DELETE SET NULL,
    FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Indexes quan trọng
CREATE INDEX idx_kpis_user_id ON kpis(user_id);
CREATE INDEX idx_kpis_year_quarter ON kpis(year, quarter);
CREATE INDEX idx_kpis_status ON kpis(status);
CREATE INDEX idx_kpis_user_year_quarter ON kpis(user_id, year, quarter);
```

**Status workflow**:
- `draft` → `submitted` → `approved` hoặc `rejected`

---

## 4. Bảng `kpi_evidence` - Minh Chứng

```sql
CREATE TABLE kpi_evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kpi_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT,
    file_size INTEGER,
    uploaded_by INTEGER NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    FOREIGN KEY (kpi_id) REFERENCES kpis(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_evidence_kpi_id ON kpi_evidence(kpi_id);
```

---

## 5. Bảng `kpi_comments` - Bình Luận

```sql
CREATE TABLE kpi_comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kpi_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kpi_id) REFERENCES kpis(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_comments_kpi_id ON kpi_comments(kpi_id);
```

---

## 6. Bảng `kpi_history` - Lịch Sử Thay Đổi

```sql
CREATE TABLE kpi_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kpi_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    action TEXT NOT NULL,  -- created, updated, submitted, approved, rejected
    old_value TEXT,  -- JSON
    new_value TEXT,  -- JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kpi_id) REFERENCES kpis(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_history_kpi_id ON kpi_history(kpi_id);
CREATE INDEX idx_history_created_at ON kpi_history(created_at);
```

---

## 7. Bảng `notifications` - Thông Báo

```sql
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT,
    message TEXT,
    type TEXT,  -- info, warning, success, error
    is_read BOOLEAN DEFAULT FALSE,
    link TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
```

---

## 8. Bảng `system_settings` - Cài Đặt Hệ Thống

```sql
CREATE TABLE system_settings (
    key TEXT PRIMARY KEY,
    value TEXT,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Database Initialization Script

```python
# scripts/init_db.py
from app.database import engine
from app.models import Base

# Create all tables
Base.metadata.create_all(bind=engine)

# Enable WAL mode
conn = engine.raw_connection()
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA synchronous=NORMAL")
conn.execute("PRAGMA cache_size=10000")
conn.close()

print("Database initialized successfully!")
```

---

## Sample Data Queries

### Tạo user mới
```sql
INSERT INTO users (email, username, password_hash, full_name, role, department, position)
VALUES ('admin@company.com', 'admin', '$2b$12$...', 'Admin User', 'admin', 'IT', 'Administrator');
```

### Tạo KPI
```sql
INSERT INTO kpis (user_id, year, quarter, title, category, target_value, status)
VALUES (1, 2024, 'Q1', 'Improve website uptime', 'goal', '99.9', 'draft');
```

### Lấy KPIs của user trong Q1/2024
```sql
SELECT k.*, u.full_name as user_name
FROM kpis k
JOIN users u ON k.user_id = u.id
WHERE k.user_id = 1 AND k.year = 2024 AND k.quarter = 'Q1';
```

### Lấy KPIs pending approval
```sql
SELECT k.*, u.full_name
FROM kpis k
JOIN users u ON k.user_id = u.id
WHERE k.status = 'submitted'
ORDER BY k.submitted_at DESC;
```

---

## Data Validation Rules

### Users
- Email: Must be unique, valid format
- Username: Must be unique, alphanumeric
- Role: Must be one of: admin, manager, employee
- Password: Min 8 chars (enforced in application)

### KPIs
- Year: Must be valid year (2020-2100)
- Quarter: Must be Q1, Q2, Q3, or Q4
- Status: Must be draft, submitted, approved, or rejected
- Progress: 0-100 (percentage)

### Files
- Max size: 50MB
- Allowed types: pdf, doc, docx, xls, xlsx, ppt, pptx, jpg, jpeg, png, gif

---

## Migration Strategy

### Using Alembic

```bash
# Create migration
alembic revision --autogenerate -m "Add new column"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Database Maintenance

### Backup
```bash
# Simple backup
cp data/database/kpi.db data/backups/kpi_$(date +%Y%m%d).db

# With SQLite command
sqlite3 data/database/kpi.db ".backup data/backups/kpi_$(date +%Y%m%d).db"
```

### Optimize
```sql
VACUUM;  -- Compact database
ANALYZE; -- Update statistics
```

### Check integrity
```sql
PRAGMA integrity_check;
```

---

**Tham khảo**: [Kiến Trúc](./02_KIEN_TRUC.md) | [API Docs](./API_SPECIFICATION.md)
