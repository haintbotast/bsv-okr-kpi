# Best Practices Bảo Mật - Hệ Thống Quản Lý KPI

---

## 1. AUTHENTICATION (Xác Thực)

✅ **JWT Tokens**:
- Secret key tối thiểu 32 ký tự
- Access token: 8 giờ
- Refresh token: 7 ngày
- Lưu token trong httpOnly cookies (khuyến nghị) hoặc localStorage

✅ **Passwords**:
- bcrypt với cost factor 12+
- Tối thiểu 8 ký tự
- Khuyến nghị: 12+ ký tự, chữ hoa/thường, số, ký tự đặc biệt
- Password reset qua email

---

## 2. AUTHORIZATION (Phân Quyền)

✅ **RBAC (Role-Based Access Control)**:
```python
# Admin: Full access
# Manager: Approve KPIs, view team data
# Employee: Own KPIs only
```

✅ **Permission Checks**:
- Validate ở mọi API endpoint
- Dùng dependency injection
- Không tin client-side checks

---

## 3. FILE UPLOADS

✅ **Validation**:
- Whitelist file types: pdf, doc, docx, xls, xlsx, ppt, pptx, jpg, jpeg, png, gif
- Max size: 50MB
- Sanitize filenames
- Dùng UUID cho filename

✅ **Storage**:
- Lưu ngoài web root
- Không execute files
- Nginx serves với security headers

---

## 4. DATABASE

✅ **Security**:
- Parameterized queries (SQLAlchemy ORM)
- Foreign key constraints
- Input validation (Pydantic)
- Regular backups

---

## 5. API SECURITY

✅ **Best Practices**:
- CORS: Whitelist domains only
- Input validation: Pydantic schemas
- SQL injection prevention: ORM
- XSS prevention: React auto-escaping
- CSRF protection (nếu dùng cookies)
- Rate limiting (optional)

---

## 6. DEPLOYMENT

✅ **Production Checklist**:
- [ ] HTTPS (Let's Encrypt)
- [ ] Strong SECRET_KEY
- [ ] Disable API docs in production
- [ ] Configure firewall (ports 80, 443 only)
- [ ] Regular security updates
- [ ] Automated backups
- [ ] Log rotation
- [ ] Monitor logs for suspicious activity

---

## 7. SENSITIVE DATA

❌ **KHÔNG BAO GIỜ**:
- Commit .env file
- Hard-code secrets
- Log passwords/tokens
- Expose stack traces to users
- Use default credentials

✅ **LÀM**:
- Dùng environment variables
- Rotate secrets định kỳ
- Encrypt backups
- Review logs thường xuyên

---

**Tham khảo**: [OWASP Top 10](https://owasp.org/www-project-top-ten/)
