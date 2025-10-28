# Chiến Lược Testing - Hệ Thống Quản Lý KPI

---

## Backend Tests (pytest)

### Unit Tests
```python
# tests/test_auth.py
def test_login_success(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "user@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

# tests/test_kpi.py
def test_create_kpi(client, auth_headers):
    response = client.post("/api/v1/kpis", 
        json={"title": "Test KPI", "year": 2024, "quarter": "Q1"},
        headers=auth_headers
    )
    assert response.status_code == 201
```

### Run Tests
```bash
cd backend
pytest
pytest --cov=app tests/  # With coverage
pytest -v tests/test_auth.py  # Specific file
```

**Target**: >70% code coverage

---

## Frontend Tests (Optional)

```javascript
// KPICard.test.jsx
test('renders KPI title', () => {
  render(<KPICard title="Test KPI" />);
  expect(screen.getByText('Test KPI')).toBeInTheDocument();
});
```

```bash
cd frontend
npm test
```

---

## Manual Testing Checklist

### Authentication
- [ ] User can register (if enabled)
- [ ] User can login
- [ ] User can logout
- [ ] Token refresh works
- [ ] Password reset works

### KPI Management
- [ ] Create KPI
- [ ] Edit KPI
- [ ] Delete KPI (draft only)
- [ ] Submit for approval
- [ ] Approve KPI (manager)
- [ ] Reject KPI (manager)
- [ ] View KPI history

### File Management
- [ ] Upload file (valid types)
- [ ] Upload rejected (invalid type)
- [ ] Upload rejected (>50MB)
- [ ] Download file
- [ ] Delete file
- [ ] Preview PDF
- [ ] Preview image

### Reports
- [ ] Generate PDF report
- [ ] Generate Excel report
- [ ] Reports contain correct data

### UI/UX
- [ ] Responsive on mobile
- [ ] Works on Chrome, Firefox, Safari
- [ ] No console errors
- [ ] Loading states display
- [ ] Error messages clear
- [ ] Success messages display

---

## E2E Tests (Playwright/Cypress)

```javascript
// e2e/kpi-workflow.spec.js
test('complete KPI workflow', async ({ page }) => {
  // Login
  await page.goto('/login');
  await page.fill('#email', 'employee@test.com');
  await page.fill('#password', 'password123');
  await page.click('button[type="submit"]');
  
  // Create KPI
  await page.click('text=Create KPI');
  await page.fill('#title', 'Test KPI');
  await page.selectOption('#quarter', 'Q1');
  await page.click('button:text("Save")');
  
  // Submit for approval
  await page.click('text=Submit');
  await page.click('text=Confirm');
  
  // Verify status
  await expect(page.locator('.status')).toHaveText('Submitted');
});
```

---

## Performance Testing

```bash
# Load test with Apache Bench
ab -n 1000 -c 30 http://localhost:8000/api/v1/kpis

# Target:
# - Response time: <500ms (p95)
# - Throughput: >100 req/s
# - Error rate: <1%
```

---

## Security Testing

### Checklist
- [ ] SQL injection attempts fail
- [ ] XSS attempts blocked
- [ ] CSRF protection works
- [ ] File upload validation works
- [ ] Authorization checks work
- [ ] Sensitive data not exposed in errors

### Tools
- OWASP ZAP (automated scan)
- Burp Suite (manual testing)

---

**Test before every deployment!**
