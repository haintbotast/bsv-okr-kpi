# SMTP Email Configuration Guide

## Quick Setup Options

### Option 1: Gmail (Recommended for Testing)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Create an App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Generate password
   - Copy the 16-character password

3. **Update your `.env` file** (or environment variables):
```bash
SMTP_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password  # NOT your regular password!
SMTP_FROM=noreply@your-company.com
SMTP_TLS=true
```

4. **Restart backend**:
```bash
docker restart kpi-backend
```

---

### Option 2: Outlook/Office 365

```bash
SMTP_ENABLED=true
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
SMTP_FROM=your-email@outlook.com
SMTP_TLS=true
```

---

### Option 3: SendGrid (For Production)

1. Sign up at https://sendgrid.com (Free tier: 100 emails/day)
2. Create an API key
3. Configure:

```bash
SMTP_ENABLED=true
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey  # Literally "apikey"
SMTP_PASSWORD=your-sendgrid-api-key
SMTP_FROM=noreply@your-verified-domain.com
SMTP_TLS=true
```

---

### Option 4: Mailgun (For Production)

1. Sign up at https://mailgun.com (Free tier: 5,000 emails/month)
2. Get SMTP credentials from dashboard
3. Configure:

```bash
SMTP_ENABLED=true
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=postmaster@your-domain.mailgun.org
SMTP_PASSWORD=your-mailgun-smtp-password
SMTP_FROM=noreply@your-domain.com
SMTP_TLS=true
```

---

### Option 5: Custom SMTP Server

```bash
SMTP_ENABLED=true
SMTP_HOST=smtp.your-server.com
SMTP_PORT=587  # or 465 for SSL, 25 for plain
SMTP_USER=your-username
SMTP_PASSWORD=your-password
SMTP_FROM=noreply@your-domain.com
SMTP_TLS=true  # or false for SSL/plain
```

---

## Testing Your Configuration

### Method 1: Using the Test Script

```bash
# Inside Docker container
docker exec -it kpi-backend python scripts/test_email.py

# Or from host (if Python installed)
cd backend
python scripts/test_email.py
```

The script will:
1. ✅ Verify SMTP configuration
2. ✅ Test all 6 email templates
3. ✅ Send a test email to your address

---

### Method 2: Using curl

```bash
# After setting up SMTP, trigger a real notification
# (requires existing user and KPI)

# Get your auth token first
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@company.com","password":"your-password"}' \
  | jq -r '.access_token')

# Update your notification preferences to ensure emails enabled
curl -X PUT http://localhost:8000/api/v1/preferences/notification-preferences \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email_notifications": true,
    "notify_kpi_submitted": true,
    "notify_kpi_approved": true,
    "notify_kpi_rejected": true,
    "notify_comment_mention": true,
    "weekly_digest": true
  }'
```

---

## Troubleshooting

### Problem: "SMTP is DISABLED"
**Solution**: Set `SMTP_ENABLED=true` in `.env` and restart container

### Problem: "Authentication failed"
**Solutions**:
- **Gmail**: Make sure you're using App Password, not regular password
- **Gmail**: Enable "Less secure app access" (if not using 2FA)
- **Outlook**: Check if account requires app-specific password
- **All**: Double-check username/password are correct

### Problem: "Connection refused" or "Timeout"
**Solutions**:
- Check if port 587 (or 465/25) is open
- Try different ports: 587 (TLS), 465 (SSL), 25 (plain)
- Check firewall settings
- Verify SMTP host is correct

### Problem: Emails go to spam
**Solutions**:
- Use a verified "From" address
- Set up SPF/DKIM records (for production)
- Use a dedicated email service (SendGrid, Mailgun)
- Avoid spam trigger words in subject/body

### Problem: "TLS/SSL error"
**Solutions**:
- Try `SMTP_TLS=false` and `SMTP_PORT=465` for SSL
- Try `SMTP_TLS=false` and `SMTP_PORT=25` for plain
- Update SSL certificates on server

---

## Docker Environment Variables

If you're using Docker, you can set environment variables in:

### Option A: Update deployment/docker-compose.yml

```yaml
services:
  backend:
    environment:
      - SMTP_ENABLED=true
      - SMTP_HOST=smtp.gmail.com
      - SMTP_PORT=587
      - SMTP_USER=${SMTP_USER}
      - SMTP_PASSWORD=${SMTP_PASSWORD}
      - SMTP_FROM=${SMTP_FROM}
```

### Option B: Create .env file in deployment/

```bash
# deployment/.env
SMTP_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@company.com
```

Then restart:
```bash
docker-compose -f deployment/docker-compose.yml down
docker-compose -f deployment/docker-compose.yml up -d
```

---

## Production Recommendations

For production deployments:

1. **Use a dedicated email service** (SendGrid, Mailgun, AWS SES)
   - Better deliverability
   - Built-in analytics
   - Handle bounces/complaints
   - Free tiers available

2. **Set up email authentication**:
   - SPF record
   - DKIM signing
   - DMARC policy

3. **Monitor email metrics**:
   - Delivery rate
   - Open rate
   - Bounce rate
   - Complaint rate

4. **Implement rate limiting**:
   - Prevent spam
   - Stay within provider limits
   - (We'll add this in Phase C.0.4!)

5. **Use environment variables**:
   - Never commit credentials
   - Use secrets management (AWS Secrets Manager, etc.)

---

## Testing Checklist

- [ ] SMTP_ENABLED=true
- [ ] Valid SMTP credentials configured
- [ ] Backend restarted after config change
- [ ] Test script runs without errors
- [ ] Test email received (check spam folder)
- [ ] Email displays correctly (HTML rendering)
- [ ] Links in email work
- [ ] Email sent from correct "From" address
- [ ] All 6 email templates work
- [ ] User notification preferences respected

---

## Next Steps After Testing

Once email is working:

1. **Integrate with KPI workflow**:
   - Update KPI service to use notification_service
   - Test KPI submission → email sent to managers
   - Test KPI approval → email sent to owner

2. **Add weekly digest job**:
   - Create background task
   - Run every Monday
   - Send summary to users with weekly_digest=true

3. **Monitor email logs**:
   - Check backend logs for email sending status
   - Set up alerting for email failures

4. **Create frontend UI**:
   - Notification preferences page
   - Test notification button
   - Email preview/testing

---

## Quick Start (TL;DR)

**For Gmail:**
1. Get App Password from https://myaccount.google.com/apppasswords
2. Update .env: `SMTP_ENABLED=true`, `SMTP_USER=your@gmail.com`, `SMTP_PASSWORD=app-password`
3. Restart: `docker restart kpi-backend`
4. Test: `docker exec -it kpi-backend python scripts/test_email.py`
5. Check inbox!
