# Mục Lục Tài Liệu - Hệ Thống Quản Lý KPI

Chào mừng đến với tài liệu Hệ Thống Quản Lý KPI!

---

## 📚 Cấu Trúc Tài Liệu

### Bắt Đầu
- [README chính](../README.md) - Tổng quan dự án và hướng dẫn nhanh
- [Hướng Dẫn Nhanh](../QUICK_START_GUIDE.md) - Workflow từng bước với Claude Code
- [Cấu hình môi trường](../.env.example) - Template biến môi trường

### Kiến Trúc & Thiết Kế
1. [**01_OVERVIEW.md**](./01_OVERVIEW.md) - Tổng quan dự án, mục tiêu và yêu cầu nghiệp vụ
2. [**02_KIEN_TRUC.md**](./02_KIEN_TRUC.md) - Kiến trúc hệ thống và các quyết định kỹ thuật
3. [**03_DATABASE_SCHEMA.md**](./03_DATABASE_SCHEMA.md) - Schema cơ sở dữ liệu đầy đủ
4. [**04_FEATURES_PHASES.md**](./04_FEATURES_PHASES.md) - Tính năng theo 7 giai đoạn phát triển

### Bảo Mật & Chất Lượng
5. [**05_BAO_MAT.md**](./05_BAO_MAT.md) - Best practices và hướng dẫn bảo mật
6. [**06_TESTING.md**](./06_TESTING.md) - Chiến lược testing và quy trình

### Vận Hành
7. [**07_DEPLOYMENT.md**](./07_DEPLOYMENT.md) - Hướng dẫn deployment và triển khai
8. [**08_BAO_TRI.md**](./08_BAO_TRI.md) - Bảo trì và xử lý sự cố

### Tài Liệu API
9. [**API_SPECIFICATION.md**](./API_SPECIFICATION.md) - Tài liệu REST API đầy đủ

---

## 🚀 Điều Hướng Nhanh

**Tôi là developer mới bắt đầu:**
→ Bắt đầu với [Hướng Dẫn Nhanh](../QUICK_START_GUIDE.md)

**Tôi muốn hiểu hệ thống:**
→ Đọc [01_OVERVIEW.md](./01_OVERVIEW.md)

**Tôi đang implement tính năng:**
→ Xem [04_FEATURES_PHASES.md](./04_FEATURES_PHASES.md) và [API_SPECIFICATION.md](./API_SPECIFICATION.md)

**Tôi đang deploy production:**
→ Làm theo [07_DEPLOYMENT.md](./07_DEPLOYMENT.md)

**Tôi cần troubleshoot:**
→ Xem [08_BAO_TRI.md](./08_BAO_TRI.md)

---

## 📦 Tài Nguyên Bổ Sung

### Files Cấu Hình
- [docker-compose.yml](../docker-compose.yml) - Cấu hình Docker cho development
- [docker-compose.prod.yml](../docker-compose.prod.yml) - Cấu hình Docker cho production
- [.env.example](../.env.example) - Template biến môi trường
- [.gitignore](../.gitignore) - Quy tắc Git ignore
- [nginx.prod.conf](../nginx.prod.conf) - Cấu hình Nginx production

### Đóng Góp
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Hướng dẫn đóng góp cho dự án
- [CHANGELOG.md](../CHANGELOG.md) - Lịch sử phiên bản

---

## 🔍 Tài Liệu Là Gì?

| Tài liệu | Mục đích | Đối tượng |
|----------|----------|-----------|
| README.md | Hướng dẫn nhanh và tổng quan | Tất cả mọi người |
| QUICK_START_GUIDE.md | Cách dùng Claude Code | Developers |
| 01_OVERVIEW.md | Tổng quan nghiệp vụ và kỹ thuật | Product owners, Developers |
| 02_KIEN_TRUC.md | Kiến trúc kỹ thuật | Developers, DevOps |
| 03_DATABASE_SCHEMA.md | Thiết kế database | Backend developers |
| 04_FEATURES_PHASES.md | Lộ trình phát triển | Developers, Project managers |
| 05_BAO_MAT.md | Hướng dẫn bảo mật | Developers, Security team |
| 06_TESTING.md | Quy trình testing | QA, Developers |
| 07_DEPLOYMENT.md | Cách triển khai | DevOps, System admins |
| 08_BAO_TRI.md | Troubleshooting & bảo trì | Support team, DevOps |
| API_SPECIFICATION.md | Tài liệu API | Frontend & Backend developers |

---

## 💡 Mẹo

- Bắt đầu với `01_OVERVIEW.md` để hiểu tổng thể
- Dùng `API_SPECIFICATION.md` làm tài liệu tham khảo chính khi phát triển
- Giữ `QUICK_START_GUIDE.md` bên tay cho Claude Code workflows
- Tham khảo file gốc `CLAUDE_CODE_PROMPT_KPI_System.txt` để xem specification đầy đủ

---

## 🆘 Cần Giúp Đỡ?

1. Kiểm tra phần tài liệu liên quan ở trên
2. Xem [Troubleshooting](./08_BAO_TRI.md#common-issues--solutions)
3. Tìm trong [README chính](../README.md) phần FAQ
4. Liên hệ: support@company.com

---

## 📝 Trạng Thái Tài Liệu

✅ = Hoàn thành | 🚧 = Đang làm | ⏳ = Dự kiến

| Tài liệu | Trạng thái |
|----------|-----------|
| README.md (Chính) | ✅ |
| QUICK_START_GUIDE.md | ✅ |
| 01_OVERVIEW.md | ✅ |
| 02_KIEN_TRUC.md | ✅ |
| 03_DATABASE_SCHEMA.md | ✅ |
| 04_FEATURES_PHASES.md | ✅ |
| 05_BAO_MAT.md | ✅ |
| 06_TESTING.md | ✅ |
| 07_DEPLOYMENT.md | ✅ |
| 08_BAO_TRI.md | ✅ |
| API_SPECIFICATION.md | ✅ |
| CONTRIBUTING.md | ✅ |
| CHANGELOG.md | ✅ |

---

**Lưu ý:** File gốc `CLAUDE_CODE_PROMPT_KPI_System.txt` chứa specification đầy đủ. Các file tài liệu này là phiên bản được tổ chức để dễ điều hướng và tham khảo.

---

**Chúc bạn code vui vẻ!** 🎉
