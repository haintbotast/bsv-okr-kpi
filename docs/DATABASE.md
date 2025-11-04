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

## Business Logic & State Machines

### KPI Status Workflow

```
┌─────────┐
│  DRAFT  │ ← Initial state when KPI created
└────┬────┘
     │
     │ submit() - Employee/Manager submits for approval
     ↓
┌────────────┐
│ SUBMITTED  │ ← Waiting for manager approval
└─────┬──────┘
      │
      ├─────→ approve() (Manager only) ─────→ ┌──────────┐
      │                                        │ APPROVED │
      │                                        └──────────┘
      │
      └─────→ reject() (Manager only) ──────→ ┌──────────┐
                                               │ REJECTED │
                                               └──────────┘
```

**State Transition Rules:**

| From State | To State  | Who Can Perform | Conditions |
|------------|-----------|----------------|------------|
| draft      | submitted | Owner, Manager | KPI must have title, category, target_value |
| submitted  | approved  | Manager, Admin | Must provide approval comment |
| submitted  | rejected  | Manager, Admin | Must provide rejection reason |
| rejected   | draft     | Owner          | Can edit and resubmit |
| approved   | -         | No one         | Final state (cannot change) |

**Implementation Logic:**

```python
# app/services/kpi_service.py

class KPIService:
    def submit_for_approval(self, kpi_id: int, user: User) -> KPI:
        """Submit KPI for manager approval."""
        kpi = self.get_kpi(kpi_id)

        # Check ownership or manager role
        if kpi.user_id != user.id and user.role not in ['admin', 'manager']:
            raise AuthorizationError("Cannot submit this KPI")

        # Validate required fields
        if not kpi.title or not kpi.category or not kpi.target_value:
            raise ValidationError("Missing required fields")

        # Check current status
        if kpi.status != 'draft':
            raise InvalidStateError(f"Cannot submit KPI in {kpi.status} status")

        # Update status
        kpi.status = 'submitted'
        kpi.submitted_at = datetime.utcnow()

        # Create history record
        self.create_history(kpi, user, 'submitted')

        # Send notification to manager
        self.notify_manager(kpi)

        return kpi

    def approve_kpi(self, kpi_id: int, manager: User, comment: str) -> KPI:
        """Approve KPI (manager only)."""
        kpi = self.get_kpi(kpi_id)

        # Check manager role
        if manager.role not in ['admin', 'manager']:
            raise AuthorizationError("Only managers can approve KPIs")

        # Check current status
        if kpi.status != 'submitted':
            raise InvalidStateError(f"Cannot approve KPI in {kpi.status} status")

        # Update status
        kpi.status = 'approved'
        kpi.approved_at = datetime.utcnow()
        kpi.approved_by = manager.id

        # Create history record
        self.create_history(kpi, manager, 'approved', comment)

        # Send notification to owner
        self.notify_user(kpi.user_id, f"Your KPI '{kpi.title}' has been approved")

        return kpi
```

### Progress Calculation Logic

**Automatic Progress Calculation:**

```python
def calculate_progress(target_value: str, current_value: str, measurement_method: str) -> float:
    """Calculate KPI progress percentage."""

    if measurement_method == 'percentage':
        # Current value is already a percentage
        return min(float(current_value), 100.0)

    elif measurement_method == 'number':
        # Calculate percentage of target reached
        target = float(target_value)
        current = float(current_value)
        return min((current / target) * 100, 100.0)

    elif measurement_method == 'boolean':
        # 0% or 100%
        return 100.0 if current_value.lower() in ['true', 'yes', '1'] else 0.0

    return 0.0

# Triggered on KPI update
def update_kpi(kpi_id: int, data: KPIUpdate) -> KPI:
    kpi = get_kpi(kpi_id)

    # Update fields
    if data.current_value:
        kpi.current_value = data.current_value
        # Auto-calculate progress
        kpi.progress_percentage = calculate_progress(
            kpi.target_value,
            data.current_value,
            kpi.measurement_method
        )

    return kpi
```

### Permission Matrix

| Action | Admin | Manager (Own Team) | Manager (Other Team) | Employee (Own) | Employee (Other) |
|--------|-------|-------------------|---------------------|---------------|------------------|
| **View KPI** | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Create KPI** | ✅ | ✅ | ❌ | ✅ | ❌ |
| **Edit Draft** | ✅ | ✅ (own) | ❌ | ✅ (own) | ❌ |
| **Edit Submitted** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Delete Draft** | ✅ | ✅ (own) | ❌ | ✅ (own) | ❌ |
| **Submit** | ✅ | ✅ (own) | ❌ | ✅ (own) | ❌ |
| **Approve** | ✅ | ✅ (team) | ❌ | ❌ | ❌ |
| **Reject** | ✅ | ✅ (team) | ❌ | ❌ | ❌ |
| **Upload File** | ✅ | ✅ (own) | ❌ | ✅ (own) | ❌ |
| **Add Comment** | ✅ | ✅ | ✅ | ✅ (own) | ❌ |
| **View Reports** | ✅ (all) | ✅ (team) | ❌ | ✅ (own) | ❌ |

**Implementation:**

```python
# app/services/permissions.py

def can_view_kpi(user: User, kpi: KPI) -> bool:
    """Check if user can view KPI."""
    if user.role == 'admin':
        return True
    if user.role == 'manager':
        return True  # Managers can view all KPIs
    return kpi.user_id == user.id  # Employees can only view their own

def can_edit_kpi(user: User, kpi: KPI) -> bool:
    """Check if user can edit KPI."""
    if user.role == 'admin':
        return True
    if kpi.status not in ['draft']:
        return False  # Can only edit drafts
    return kpi.user_id == user.id  # Only owner can edit

def can_approve_kpi(user: User, kpi: KPI) -> bool:
    """Check if user can approve KPI."""
    if user.role == 'admin':
        return True
    if user.role == 'manager' and kpi.status == 'submitted':
        return True
    return False
```

### Data Integrity Rules

**Cascade Delete Behaviors:**

```sql
-- When user is deleted:
- CASCADE: All their KPIs are deleted
- CASCADE: All their comments are deleted
- CASCADE: All their uploaded files are deleted
- CASCADE: All their notifications are deleted
- SET NULL: KPIs they approved remain but approved_by = NULL

-- When KPI is deleted:
- CASCADE: All evidence files are deleted
- CASCADE: All comments are deleted
- CASCADE: All history records are deleted

-- When template is deleted:
- SET NULL: KPIs using it remain but template_id = NULL
```

**Unique Constraints:**

```sql
-- Prevent duplicate KPIs for same user/quarter
CREATE UNIQUE INDEX idx_user_kpi_unique
ON kpis(user_id, year, quarter, title);

-- Prevent duplicate usernames/emails
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE UNIQUE INDEX idx_users_username ON users(username);
```

### Calculated Fields

**Fields that are auto-calculated:**

1. **progress_percentage** - Calculated from target_value and current_value
2. **updated_at** - Auto-updated on every change
3. **submitted_at** - Set when status changes to 'submitted'
4. **approved_at** - Set when status changes to 'approved'

**Triggers (if needed):**

```sql
-- Update updated_at timestamp automatically
CREATE TRIGGER update_kpi_timestamp
AFTER UPDATE ON kpis
BEGIN
    UPDATE kpis SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;
```

### Sample Data for Testing

```sql
-- Insert test users
INSERT INTO users (email, username, password_hash, full_name, role, department, position) VALUES
('admin@company.com', 'admin', '$2b$12$...', 'Admin User', 'admin', 'IT', 'System Admin'),
('manager@company.com', 'manager1', '$2b$12$...', 'John Manager', 'manager', 'IT', 'Team Lead'),
('emp1@company.com', 'employee1', '$2b$12$...', 'Alice Employee', 'employee', 'IT', 'Developer'),
('emp2@company.com', 'employee2', '$2b$12$...', 'Bob Employee', 'employee', 'IT', 'Developer');

-- Insert KPI templates
INSERT INTO kpi_templates (name, description, category, role, measurement_method, target_type, created_by) VALUES
('Server Uptime', 'Maintain server uptime percentage', 'goal', 'employee', 'percentage', 'percentage', 1),
('Bug Fixes', 'Number of bugs fixed per quarter', 'task', 'employee', 'number', 'number', 1),
('Project Completion', 'Complete assigned project', 'mission', 'manager', 'boolean', 'boolean', 1);

-- Insert sample KPIs
INSERT INTO kpis (user_id, template_id, year, quarter, title, description, category, target_value, current_value, progress_percentage, measurement_method, status) VALUES
(3, 1, 2024, 'Q1', 'Improve website uptime', 'Achieve 99.9% uptime', 'goal', '99.9', '99.5', 99.5, 'percentage', 'submitted'),
(3, 2, 2024, 'Q1', 'Fix critical bugs', 'Fix 50 critical bugs', 'task', '50', '35', 70, 'number', 'approved'),
(4, 1, 2024, 'Q1', 'Database performance', 'Optimize database queries', 'goal', '95', '0', 0, 'percentage', 'draft');

-- Insert system settings
INSERT INTO system_settings (key, value, description) VALUES
('app_name', 'KPI Management System', 'Application name'),
('allow_registration', 'false', 'Allow public user registration'),
('max_file_size', '52428800', 'Maximum file upload size in bytes (50MB)'),
('notification_retention_days', '30', 'Days to keep read notifications');
```

---

**Tham khảo**: [ARCHITECTURE.md](./ARCHITECTURE.md) | [technical/SCHEMAS.md](./technical/SCHEMAS.md)
