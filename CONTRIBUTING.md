# Đóng Góp Cho Hệ Thống Quản Lý KPI

Cảm ơn bạn quan tâm đến việc đóng góp cho Hệ Thống Quản Lý KPI! Tài liệu này cung cấp hướng dẫn và quy trình để đóng góp cho dự án.

---

## Mục Lục

1. [Quy Tắc Ứng Xử](#quy-tắc-ứng-xử)
2. [Bắt Đầu](#bắt-đầu)
3. [Quy Trình Phát Triển](#quy-trình-phát-triển)
4. [Chuẩn Lập Trình](#chuẩn-lập-trình)
5. [Yêu Cầu Testing](#yêu-cầu-testing)
6. [Hướng Dẫn Commit](#hướng-dẫn-commit)
7. [Quy Trình Pull Request](#quy-trình-pull-request)
8. [Tài Liệu](#tài-liệu)
9. [Báo Cáo Issues](#báo-cáo-issues)

---

## Quy Tắc Ứng Xử

Dự án này tuân theo quy tắc ứng xử chuẩn:

- Tôn trọng và hòa nhập
- Chào đón người mới
- Tập trung vào phản hồi mang tính xây dựng
- Tôn trọng quan điểm khác nhau
- Ưu tiên lợi ích tốt nhất của cộng đồng

---

## Bắt Đầu

### Yêu Cầu

Trước khi bắt đầu, đảm bảo bạn đã cài:

- **Git**
- **Docker** và **Docker Compose**
- **Python 3.11+** (cho phát triển backend)
- **Node.js 18+** và **npm** (cho phát triển frontend)
- Code editor (VS Code, PyCharm, v.v.)

### Thiết Lập Môi Trường Phát Triển

```bash
# Clone repository
git clone https://github.com/your-org/kpi-system.git
cd kpi-system

# Tạo file môi trường
cp .env.example .env
# Chỉnh sửa .env với cài đặt local

# Khởi động môi trường development
docker-compose up -d

# Hoặc chạy locally:

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## Quy Trình Phát Triển

### 1. Tạo Branch

Luôn tạo branch mới cho thay đổi của bạn:

```bash
git checkout -b feature/ten-tinh-nang
# hoặc
git checkout -b fix/mo-ta-bug
```

Quy ước đặt tên branch:
- `feature/` - Tính năng mới
- `fix/` - Sửa bug
- `docs/` - Cập nhật tài liệu
- `refactor/` - Refactoring code
- `test/` - Thêm tests
- `chore/` - Công việc bảo trì

### 2. Thực Hiện Thay Đổi

- Viết code sạch, dễ đọc
- Tuân theo chuẩn lập trình (xem bên dưới)
- Thêm tests cho tính năng mới
- Cập nhật tài liệu nếu cần

### 3. Test Thay Đổi

```bash
# Backend tests
cd backend
pytest

# Frontend tests (nếu có)
cd frontend
npm test

# Integration test đầy đủ
docker-compose up -d
# Test thủ công trong browser
```

### 4. Commit Thay Đổi

Tuân theo hướng dẫn commit (xem bên dưới).

### 5. Push và Tạo Pull Request

```bash
git push origin feature/ten-tinh-nang
```

Sau đó tạo Pull Request trên GitHub/GitLab.

---

## Chuẩn Lập Trình

### Python (Backend)

**Style Guide**: Tuân theo PEP 8

```python
# Tốt
def calculate_progress(current: float, target: float) -> float:
    """Tính phần trăm tiến độ.

    Args:
        current: Giá trị hiện tại
        target: Giá trị mục tiêu

    Returns:
        Tiến độ dạng phần trăm (0-100)
    """
    if target == 0:
        return 0
    return (current / target) * 100

# Không tốt
def calc(c,t):
    return c/t*100 if t!=0 else 0
```

**Điểm Quan Trọng**:
- Dùng type hints
- Viết docstrings cho functions/classes
- Độ dài dòng tối đa: 100 ký tự
- Dùng tên biến mô tả rõ ràng
- Tuân theo best practices của FastAPI

**Tools**:
```bash
# Format code
black app/

# Kiểm tra style
flake8 app/

# Sắp xếp imports
isort app/
```

### JavaScript/React (Frontend)

**Style Guide**: Airbnb JavaScript Style Guide

```javascript
// Tốt
const calculateProgress = (current, target) => {
  if (target === 0) return 0;
  return (current / target) * 100;
};

// Không tốt
function calc(c,t){return t!=0?c/t*100:0}
```

**Điểm Quan Trọng**:
- Dùng functional components với hooks
- Dùng ESLint và Prettier
- Dùng tên component có ý nghĩa
- Giữ components nhỏ và tập trung
- Thêm PropTypes hoặc TypeScript types

**Tools**:
```bash
# Format code
npm run format

# Lint code
npm run lint

# Sửa lỗi lint
npm run lint:fix
```

### Hướng Dẫn Chung

- **DRY** (Don't Repeat Yourself)
- **KISS** (Keep It Simple, Stupid)
- **YAGNI** (You Aren't Gonna Need It)
- Viết code tự giải thích
- Comment cho logic phức tạp
- Tránh tối ưu hóa sớm

---

## Yêu Cầu Testing

### Backend Tests

Tất cả thay đổi backend nên có tests:

```python
# tests/test_kpi.py
def test_create_kpi(client, test_user):
    """Test tạo KPI."""
    response = client.post(
        "/api/v1/kpis",
        json={
            "title": "Test KPI",
            "year": 2024,
            "quarter": "Q1"
        },
        headers={"Authorization": f"Bearer {test_user.token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test KPI"
```

**Mục tiêu Coverage**: Hướng tới >70% code coverage

```bash
pytest --cov=app tests/
```

### Frontend Tests (Tùy chọn)

Nếu implement frontend tests:

```javascript
// KPICard.test.jsx
test('renders KPI card với title', () => {
  render(<KPICard title="Test KPI" />);
  expect(screen.getByText('Test KPI')).toBeInTheDocument();
});
```

### Checklist Testing Thủ Công

Trước khi submit, test thủ công:
- [ ] Tính năng hoạt động đúng
- [ ] Không có lỗi console
- [ ] Responsive trên mobile
- [ ] Hoạt động trên Chrome, Firefox, Safari
- [ ] Xử lý lỗi đúng
- [ ] Loading states hoạt động

---

## Hướng Dẫn Commit

### Format Commit Message

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: Tính năng mới
- `fix`: Sửa bug
- `docs`: Thay đổi tài liệu
- `style`: Thay đổi code style (format)
- `refactor`: Refactoring code
- `test`: Thêm tests
- `chore`: Công việc bảo trì

**Ví dụ**:

```bash
feat(kpi): thêm theo dõi tiến độ theo quý

Implement tính toán tiến độ theo quý với cập nhật tự động
khi upload minh chứng.

Closes #123
```

```bash
fix(auth): giải quyết race condition khi refresh token

Fixed vấn đề khi nhiều requests refresh đồng thời sẽ fail.
Thêm mutex lock để ngăn concurrent refreshes.

Fixes #456
```

**Quy tắc**:
- Dùng thì hiện tại ("add" không phải "added")
- Dòng đầu tối đa 72 ký tự
- Reference issue numbers
- Giải thích "tại sao" trong body, không phải "cái gì"

---

## Quy Trình Pull Request

### Trước Khi Tạo PR

1. ✅ Cập nhật từ main branch
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/tinh-nang-cua-ban
   git merge main
   ```

2. ✅ Chạy tất cả tests
3. ✅ Cập nhật tài liệu
4. ✅ Tự review code của bạn
5. ✅ Kiểm tra merge conflicts

### Template PR

Khi tạo PR, bao gồm:

```markdown
## Mô Tả
Mô tả ngắn gọn về thay đổi

## Loại Thay Đổi
- [ ] Sửa bug
- [ ] Tính năng mới
- [ ] Breaking change
- [ ] Cập nhật tài liệu

## Issues Liên Quan
Closes #123

## Testing
- [ ] Unit tests đã thêm/cập nhật
- [ ] Manual testing hoàn thành
- [ ] Tất cả tests pass

## Screenshots (nếu có)
[Thêm screenshots ở đây]

## Checklist
- [ ] Code tuân theo style guidelines
- [ ] Đã tự review
- [ ] Đã thêm comments cho code phức tạp
- [ ] Tài liệu đã cập nhật
- [ ] Không có warnings mới
- [ ] Tests pass locally
```

### Quy Trình Review

1. Tạo PR với mô tả chi tiết
2. Assign reviewers (nếu có)
3. Xử lý review comments
4. Cập nhật PR dựa trên feedback
5. Chờ approval
6. Squash and merge (hoặc rebase)

### Sau Merge

- Xóa feature branch của bạn
- Cập nhật local main branch
- Đóng issues liên quan

---

## Tài Liệu

### Code Documentation

**Python**:
```python
def calculate_kpi_progress(kpi: KPI) -> float:
    """Tính phần trăm tiến độ KPI.

    Function này tính tiến độ dựa trên current_value
    và target_value của KPI model.

    Args:
        kpi: KPI model instance

    Returns:
        float: Phần trăm tiến độ (0-100)

    Raises:
        ValueError: Nếu target_value không hợp lệ

    Example:
        >>> kpi = KPI(current_value=90, target_value=100)
        >>> calculate_kpi_progress(kpi)
        90.0
    """
    # Implementation
```

**JavaScript**:
```javascript
/**
 * Tính phần trăm tiến độ KPI
 * @param {number} current - Giá trị hiện tại
 * @param {number} target - Giá trị mục tiêu
 * @returns {number} Phần trăm tiến độ (0-100)
 */
const calculateProgress = (current, target) => {
  // Implementation
};
```

### Cập Nhật Tài Liệu

Khi thực hiện thay đổi, cập nhật:
- API documentation (nếu có thay đổi API)
- README.md (nếu có thay đổi user-facing)
- Code comments
- Inline documentation

---

## Báo Cáo Issues

### Báo Cáo Bug

Dùng template này:

```markdown
**Mô Tả Bug**
Mô tả rõ ràng về bug

**Các Bước Tái Hiện**
Các bước để tái hiện:
1. Đi tới '...'
2. Click vào '...'
3. Thấy lỗi

**Hành Vi Mong Đợi**
Bạn mong đợi điều gì xảy ra

**Screenshots**
Thêm screenshots nếu có

**Môi Trường**
- OS: [vd. Ubuntu 22.04]
- Browser: [vd. Chrome 120]
- Version: [vd. 1.0.0]

**Thông Tin Bổ Sung**
Bất kỳ thông tin liên quan nào khác
```

### Yêu Cầu Tính Năng

```markdown
**Mô Tả Tính Năng**
Mô tả rõ ràng về tính năng

**Vấn Đề Nó Giải Quyết**
Tính năng này giải quyết vấn đề gì?

**Giải Pháp Đề Xuất**
Bạn sẽ implement nó như thế nào?

**Các Phương Án Khác**
Các cách tiếp cận khác bạn đã cân nhắc

**Thông Tin Bổ Sung**
Mockups, ví dụ, v.v.
```

---

## Cấu Trúc Dự Án

Làm quen với cấu trúc:

```
kpi-system/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── models/   # SQLAlchemy models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── crud/     # CRUD operations
│   │   └── services/ # Business logic
│   └── tests/        # Backend tests
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── contexts/
│   └── public/
├── docs/             # Tài liệu
├── data/             # Dữ liệu lưu trữ (không trong Git)
└── docker-compose.yml
```

---

## Best Practices Phát Triển

### Bảo Mật
- Không bao giờ commit files `.env`
- Không hardcode secrets
- Validate tất cả user inputs
- Dùng parameterized queries
- Tuân theo hướng dẫn OWASP

### Hiệu Năng
- Tránh N+1 queries
- Dùng pagination cho lists
- Tối ưu hóa images
- Lazy load components
- Cache khi phù hợp

### Accessibility
- Dùng semantic HTML
- Thêm ARIA labels
- Hỗ trợ keyboard navigation
- Test với screen readers
- Duy trì color contrast

---

## Câu Hỏi?

- Kiểm tra [tài liệu](./docs/)
- Hỏi trong project discussions
- Liên hệ maintainers: support@company.com

---

## License

Bằng việc đóng góp, bạn đồng ý rằng contributions của bạn sẽ được licensed theo cùng license với dự án.

---

**Cảm ơn bạn đã đóng góp!** 🎉

Contributions của bạn làm dự án này tốt hơn cho mọi người.
