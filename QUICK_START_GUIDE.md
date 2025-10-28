# 🚀 QUICK START GUIDE - KPI Management System

## Cách sử dụng Prompt với Claude Code

### Bước 1: Chuẩn bị môi trường

```bash
# Cài đặt Claude Code (nếu chưa có)
# Xem: https://docs.claude.com/en/docs/claude-code

# Tạo thư mục dự án
mkdir kpi-system
cd kpi-system
```

### Bước 2: Khởi động Claude Code

```bash
# Mở Claude Code trong thư mục dự án
claude-code
```

### Bước 3: Đưa prompt vào Claude Code

**Copy toàn bộ nội dung file `CLAUDE_CODE_PROMPT_KPI_System.txt`** và paste vào Claude Code với lệnh:

```
Hãy xây dựng hệ thống KPI Management System theo specification trong prompt này. 
Bắt đầu với Phase 1: Core Infrastructure.

[PASTE TOÀN BỘ NỘI DUNG PROMPT Ở ĐÂY]
```

### Bước 4: Làm việc theo từng Phase

Claude Code sẽ bắt đầu tạo code. Bạn có thể hướng dẫn theo từng phase:

**Phase 1: Core Infrastructure**
```
Bắt đầu Phase 1: Core Infrastructure
1. Tạo cấu trúc thư mục backend và frontend
2. Setup FastAPI với SQLite
3. Tạo authentication system với JWT
4. Setup Docker Compose
```

**Phase 2: KPI Management**
```
Tiếp tục Phase 2: KPI Management
1. Implement KPI CRUD
2. Tạo dashboard page
3. Tạo KPI list và detail views
```

... và tiếp tục với các phase khác.

### Bước 5: Test từng feature

Sau mỗi phase, test các chức năng:

```bash
# Test backend
cd backend
python -m pytest

# Test frontend
cd frontend
npm run dev

# Test with Docker
docker-compose up -d
```

### Bước 6: Deploy

```bash
# Build và deploy
docker-compose up -d --build

# Initialize database
docker-compose exec backend python scripts/init_db.py

# Create admin user
docker-compose exec backend python scripts/create_admin.py \
  --email admin@company.com \
  --password "ChangeMeInProduction123!" \
  --fullname "System Admin"
```

---

## 📝 Workflow làm việc với Claude Code

### 1. Iterative Development

```
YOU: "Implement user authentication with JWT"
CLAUDE CODE: [Creates auth code]
YOU: "Test the login endpoint"
CLAUDE CODE: [Creates test]
YOU: "Fix the token refresh logic"
CLAUDE CODE: [Updates code]
```

### 2. Feature Request Pattern

```
YOU: "Add file upload feature with these requirements:
- Support PDF, DOCX, XLSX
- Max 50MB per file
- Store in /data/uploads
- Preview in browser"

CLAUDE CODE: [Implements complete feature]
```

### 3. Bug Fix Pattern

```
YOU: "Fix bug: Users can see other users' KPIs
Error appears in kpi_list view"

CLAUDE CODE: [Analyzes and fixes]
```

### 4. Code Review Pattern

```
YOU: "Review the KPI approval workflow code for security issues"

CLAUDE CODE: [Reviews and suggests improvements]
```

---

## 🎯 Best Practices

### ✅ DO:
- Làm việc theo từng phase, hoàn thành phase trước khi chuyển phase sau
- Test kỹ sau mỗi feature
- Commit code thường xuyên với message rõ ràng
- Hỏi Claude Code review code trước khi merge
- Document các quyết định quan trọng

### ❌ DON'T:
- Đừng skip testing
- Đừng cố gắng làm quá nhiều features cùng lúc
- Đừng deploy mà chưa test local
- Đừng hard-code sensitive data
- Đừng over-engineer cho 30 users

---

## 🛠️ Common Commands

### Development

```bash
# Backend development
cd backend
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
uvicorn app.main:app --reload

# Frontend development
cd frontend
npm run dev

# Run tests
pytest                    # Backend
npm test                  # Frontend (if configured)

# Database migrations
alembic revision --autogenerate -m "Description"
alembic upgrade head

# Docker
docker-compose up -d
docker-compose logs -f backend
docker-compose down
docker-compose exec backend bash
```

### Production

```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d --build

# Backup database
docker-compose exec backend python scripts/backup.py

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Update application
git pull origin main
docker-compose down
docker-compose up -d --build
docker-compose exec backend alembic upgrade head
```

---

## 🐛 Troubleshooting

### Issue: Claude Code không hiểu yêu cầu

**Solution:**
- Chia nhỏ yêu cầu thành các task cụ thể hơn
- Cung cấp ví dụ code mẫu
- Chỉ rõ file cần modify

### Issue: Code không chạy

**Solution:**
```
YOU: "Debug error: [paste error message]"
CLAUDE CODE: [Analyzes and fixes]
```

### Issue: Muốn thay đổi thiết kế

**Solution:**
```
YOU: "Refactor the KPI model to support:
- Multiple quarters in one KPI
- Quarter weights
- Auto-calculate annual progress"

CLAUDE CODE: [Implements changes]
```

---

## 📊 Progress Tracking

Tạo checklist để track progress:

```markdown
## Phase 1: Core Infrastructure ✅
- [x] Project structure
- [x] FastAPI setup
- [x] SQLite database
- [x] Authentication
- [x] Docker setup

## Phase 2: KPI Management 🔄
- [x] KPI CRUD backend
- [ ] Dashboard frontend
- [ ] KPI list view
- [ ] KPI detail view

## Phase 3: File Management ⏳
- [ ] File upload
- [ ] File preview
- [ ] File delete

...
```

---

## 💡 Tips & Tricks

### 1. Sử dụng file documentation của prompt

Trong prompt có section về Database Schema, API Endpoints, Component Structure - sử dụng chúng làm reference khi làm việc với Claude Code.

### 2. Request specific examples

```
YOU: "Show me example code for the KPI approval endpoint"
CLAUDE CODE: [Provides example]
```

### 3. Ask for explanation

```
YOU: "Explain the authentication flow in this system"
CLAUDE CODE: [Explains step by step]
```

### 4. Request refactoring

```
YOU: "Refactor the file upload code to be more modular"
CLAUDE CODE: [Refactors]
```

### 5. Generate tests

```
YOU: "Generate pytest tests for the KPI CRUD operations"
CLAUDE CODE: [Creates tests]
```

---

## 🎓 Learning Resources

### FastAPI
- https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

### React
- https://react.dev/
- https://react.dev/learn

### SQLAlchemy
- https://docs.sqlalchemy.org/
- Tutorial: https://docs.sqlalchemy.org/en/20/tutorial/

### Docker
- https://docs.docker.com/
- Compose: https://docs.docker.com/compose/

---

## 📞 Support

Nếu gặp vấn đề:

1. **Check Documentation**: Xem lại prompt specification
2. **Ask Claude Code**: "Explain why X is not working"
3. **Review Logs**: Check Docker logs hoặc application logs
4. **Search Issues**: Google error messages
5. **Simplify**: Chia nhỏ vấn đề, test từng phần

---

## ⏱️ Estimated Timeline

| Phase | Tasks | Time | Status |
|-------|-------|------|--------|
| Phase 1 | Core Infrastructure | 1 week | ⏳ |
| Phase 2 | KPI Management | 1 week | ⏳ |
| Phase 3 | File Management | 1 week | ⏳ |
| Phase 4 | Workflow & Collaboration | 1 week | ⏳ |
| Phase 5 | Reporting & Analytics | 1 week | ⏳ |
| Phase 6 | Admin Features | 1 week | ⏳ |
| Phase 7 | Optimization & Polish | 2 weeks | ⏳ |
| **Total** | | **8 weeks** | |

---

## 🎯 Success Checklist

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

1. **Đọc kỹ prompt specification** (CLAUDE_CODE_PROMPT_KPI_System.txt)
2. **Setup môi trường development**
3. **Khởi động Claude Code**
4. **Bắt đầu Phase 1**
5. **Test và iterate**
6. **Deploy to production**
7. **Train users**
8. **Collect feedback**
9. **Plan improvements**

---

**Good luck with your KPI Management System!** 🎉

Remember: Keep it simple, test thoroughly, and focus on your 30 users' needs!
