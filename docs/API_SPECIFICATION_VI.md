# Đặc Tả API - Hệ Thống Quản Lý KPI

**Phiên bản**: 1.0.0  
**Base URL**: `http://localhost:8000/api/v1`  
**Xác thực**: JWT Bearer Token

---

## Mục Lục

1. [Xác Thực](#xác-thực)
2. [Người Dùng](#người-dùng)
3. [Templates KPI](#templates-kpi)
4. [KPIs](#kpis)
5. [Files/Minh Chứng](#filesminh-chứng)
6. [Bình Luận](#bình-luận)
7. [Thông Báo](#thông-báo)
8. [Báo Cáo](#báo-cáo)
9. [Admin](#admin)
10. [Hệ Thống](#hệ-thống)

---

## Xác Thực

### POST /auth/login
Đăng nhập với email và mật khẩu.

**Request Body:**
```json
{
  "email": "user@company.com",
  "password": "SecurePassword123!"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 28800,
  "user": {
    "id": 1,
    "email": "user@company.com",
    "full_name": "Nguyễn Văn A",
    "role": "employee"
  }
}
```

**Lỗi**:
- `401`: Thông tin đăng nhập không hợp lệ
- `403`: Tài khoản bị vô hiệu hóa

### POST /auth/refresh
Làm mới access token.

### POST /auth/logout
Đăng xuất.

### POST /auth/forgot-password
Yêu cầu đặt lại mật khẩu.

### POST /auth/reset-password
Đặt lại mật khẩu với token.

---

## Người Dùng

### GET /users/me
Lấy thông tin profile người dùng hiện tại.

**Headers:**
```
Authorization: Bearer {access_token}
```

### PUT /users/me
Cập nhật profile.

### PUT /users/me/password
Đổi mật khẩu.

### GET /users
Danh sách tất cả người dùng (Admin/Manager only).

**Query Parameters:**
- `page`: Số trang (mặc định: 1)
- `page_size`: Số mục/trang (mặc định: 20)
- `role`: Lọc theo vai trò
- `department`: Lọc theo phòng ban
- `search`: Tìm kiếm theo tên/email

### POST /users (Admin only)
Tạo người dùng mới.

### PUT /users/{user_id} (Admin only)
Cập nhật người dùng.

### DELETE /users/{user_id} (Admin only)
Vô hiệu hóa người dùng (soft delete).

---

## Templates KPI

### GET /templates
Danh sách templates KPI.

### GET /templates/{template_id}
Chi tiết template.

### POST /templates (Admin only)
Tạo template mới.

### PUT /templates/{template_id} (Admin only)
Cập nhật template.

### DELETE /templates/{template_id} (Admin only)
Xóa template.

---

## KPIs

### GET /kpis
Danh sách KPIs (lọc theo vai trò người dùng).

**Query Parameters:**
- `user_id`: Lọc theo người dùng
- `year`: Lọc theo năm
- `quarter`: Lọc theo quý (Q1, Q2, Q3, Q4)
- `status`: Lọc theo trạng thái (draft, submitted, approved, rejected)
- `search`: Tìm trong title/description

**Response:** `200 OK`
```json
{
  "total": 50,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": 1,
      "user_id": 1,
      "user_name": "Nguyễn Văn A",
      "year": 2024,
      "quarter": "Q1",
      "title": "Nâng cao uptime website",
      "target_value": "99.9",
      "current_value": "99.7",
      "progress_percentage": 97.8,
      "status": "approved"
    }
  ]
}
```

### GET /kpis/{kpi_id}
Chi tiết KPI.

### POST /kpis
Tạo KPI mới.

**Request Body:**
```json
{
  "template_id": 1,
  "year": 2024,
  "quarter": "Q1",
  "title": "Nâng cao uptime website",
  "description": "Duy trì 99.9% uptime cho website công ty",
  "category": "goal",
  "target_value": "99.9",
  "measurement_method": "UptimeRobot monitoring"
}
```

### PUT /kpis/{kpi_id}
Cập nhật KPI.

### DELETE /kpis/{kpi_id}
Xóa KPI (chỉ draft).

### POST /kpis/{kpi_id}/submit
Gửi KPI để phê duyệt.

### POST /kpis/{kpi_id}/approve (Manager/Admin only)
Phê duyệt KPI.

**Request Body:**
```json
{
  "comment": "Tiến độ tốt, phê duyệt!"
}
```

### POST /kpis/{kpi_id}/reject (Manager/Admin only)
Từ chối KPI.

**Request Body:**
```json
{
  "reason": "Giá trị mục tiêu cần cụ thể hơn"
}
```

### GET /kpis/{kpi_id}/history
Lấy lịch sử thay đổi KPI.

---

## Files/Minh Chứng

### GET /kpis/{kpi_id}/evidence
Danh sách files minh chứng.

### POST /kpis/{kpi_id}/evidence
Upload file minh chứng.

**Request:**
- Content-Type: `multipart/form-data`
- Fields:
  - `file`: File binary
  - `description`: Mô tả (optional)

**Giới hạn**:
- Kích thước tối đa: 50MB
- Loại file: pdf, doc, docx, xls, xlsx, ppt, pptx, jpg, jpeg, png, gif

### GET /files/{file_id}
Download file.

### DELETE /files/{file_id}
Xóa file.

---

## Bình Luận

### GET /kpis/{kpi_id}/comments
Danh sách bình luận.

### POST /kpis/{kpi_id}/comments
Thêm bình luận.

**Request Body:**
```json
{
  "comment": "Đã cập nhật với số liệu mới nhất"
}
```

### PUT /comments/{comment_id}
Sửa bình luận (chỉ người tạo).

### DELETE /comments/{comment_id}
Xóa bình luận.

---

## Thông Báo

### GET /notifications
Danh sách thông báo.

**Response:** `200 OK`
```json
{
  "total": 10,
  "unread_count": 3,
  "items": [
    {
      "id": 1,
      "title": "KPI Đã Được Phê Duyệt",
      "message": "KPI 'Nâng cao uptime website' đã được phê duyệt",
      "type": "success",
      "is_read": false,
      "link": "/kpis/1"
    }
  ]
}
```

### PUT /notifications/{notification_id}/read
Đánh dấu đã đọc.

### PUT /notifications/read-all
Đánh dấu tất cả đã đọc.

---

## Báo Cáo

### GET /reports/user/{user_id}
Tạo báo cáo người dùng (PDF/Excel).

**Query Parameters:**
- `year`: Năm (bắt buộc)
- `quarter`: Quý (Q1, Q2, Q3, Q4, hoặc "all")
- `format`: pdf hoặc excel (mặc định: pdf)

**Response:** File download

### GET /reports/department
Báo cáo phòng ban (Manager/Admin only).

### GET /reports/company (Admin only)
Báo cáo toàn công ty.

### GET /analytics/dashboard
Lấy dữ liệu analytics cho dashboard.

**Response:** `200 OK`
```json
{
  "summary": {
    "total_kpis": 50,
    "approved_kpis": 35,
    "pending_kpis": 10,
    "average_progress": 87.5
  },
  "by_quarter": {
    "Q1": {"total": 15, "approved": 12, "avg_progress": 90.5},
    "Q2": {"total": 12, "approved": 10, "avg_progress": 85.0}
  },
  "by_department": {
    "IT": {"total": 30, "avg_progress": 88.0},
    "HR": {"total": 10, "avg_progress": 85.0}
  }
}
```

---

## Admin

### GET /admin/users
Danh sách tất cả người dùng với chi tiết admin.

### GET /admin/system-settings
Lấy cài đặt hệ thống.

### PUT /admin/system-settings
Cập nhật cài đặt.

### GET /admin/audit-log
Xem audit log.

**Query Parameters:**
- `user_id`: Lọc theo người dùng
- `action`: Lọc theo hành động
- `start_date`, `end_date`: Lọc theo thời gian

### POST /admin/backup
Kích hoạt backup thủ công.

### GET /admin/backups
Danh sách backups có sẵn.

---

## Hệ Thống

### GET /health
Kiểm tra sức khỏe hệ thống (public).

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T12:00:00Z",
  "version": "1.0.0"
}
```

### GET /version
Thông tin phiên bản API (public).

---

## Format Lỗi

Tất cả lỗi theo format:

```json
{
  "detail": "Thông báo lỗi",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-15T12:00:00Z"
}
```

### HTTP Status Codes:
- `200 OK`: Thành công
- `201 Created`: Tạo thành công
- `204 No Content`: Thành công không có nội dung
- `400 Bad Request`: Dữ liệu không hợp lệ
- `401 Unauthorized`: Cần xác thực
- `403 Forbidden`: Không đủ quyền
- `404 Not Found`: Không tìm thấy
- `409 Conflict`: Xung đột dữ liệu
- `413 Payload Too Large`: File quá lớn
- `422 Unprocessable Entity`: Lỗi validation
- `429 Too Many Requests`: Vượt giới hạn
- `500 Internal Server Error`: Lỗi server

---

## Xác Thực

Tất cả endpoints yêu cầu xác thực cần JWT token trong header:

```
Authorization: Bearer {access_token}
```

Token hết hạn sau 8 giờ. Dùng refresh token để lấy access token mới.

---

## Rate Limiting

(Tùy chọn, nếu được bật)

- Mặc định: 60 requests/phút/user
- Vượt quá trả về `429 Too Many Requests`

---

## Pagination

Các list endpoints hỗ trợ pagination:

**Query Parameters:**
- `page`: Số trang (mặc định: 1)
- `page_size`: Số mục/trang (mặc định: 20, max: 100)

**Format Response:**
```json
{
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5,
  "items": [...]
}
```

---

## Filtering & Sorting

**Query parameters chung:**
- `sort_by`: Tên field để sắp xếp
- `order`: `asc` hoặc `desc` (mặc định: desc)
- `search`: Tìm kiếm full-text

**Ví dụ:**
```
GET /api/v1/kpis?year=2024&quarter=Q1&status=approved&sort_by=created_at&order=desc
```

---

## Upload File

**Loại file cho phép:**
- Tài liệu: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX
- Hình ảnh: JPG, JPEG, PNG, GIF

**Giới hạn kích thước:** 50 MB/file

**Content-Type:** `multipart/form-data`

---

## Webhooks

Chưa được implement trong v1.0.0

---

## API Versioning

Phiên bản hiện tại: **v1**

Base URL bao gồm version: `/api/v1/`

Các phiên bản tương lai sẽ dùng: `/api/v2/`, v.v.

---

## Hỗ Trợ

- API Documentation (Swagger UI): http://localhost:8000/docs
- API Documentation (ReDoc): http://localhost:8000/redoc
- Email hỗ trợ: support@company.com

---

**Lưu ý:** Đây là phiên bản tóm tắt tiếng Việt. Xem file `API_SPECIFICATION.md` gốc để biết chi tiết đầy đủ về tất cả endpoints và examples.
