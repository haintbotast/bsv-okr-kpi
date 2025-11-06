#!/usr/bin/env python3
"""Test email notification system."""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.email import email_service
from app.utils.email_templates import (
    kpi_submitted_email,
    kpi_approved_email,
    kpi_rejected_email,
    comment_mention_email,
    password_reset_email,
    weekly_digest_email
)
from app.config import settings


def test_smtp_connection():
    """Test SMTP connection."""
    print("=" * 60)
    print("SMTP CONNECTION TEST")
    print("=" * 60)
    print(f"Enabled: {settings.SMTP_ENABLED}")
    print(f"Host: {settings.SMTP_HOST}")
    print(f"Port: {settings.SMTP_PORT}")
    print(f"User: {settings.SMTP_USER}")
    print(f"From: {settings.SMTP_FROM}")
    print(f"TLS: {settings.SMTP_TLS}")
    print()

    if not settings.SMTP_ENABLED:
        print("❌ SMTP is DISABLED in settings")
        print("Set SMTP_ENABLED=true in your .env file")
        return False

    if settings.SMTP_USER == "your-email@gmail.com":
        print("❌ SMTP credentials are placeholder values")
        print("Update SMTP_USER and SMTP_PASSWORD in your .env file")
        return False

    print("✅ SMTP configuration looks good")
    return True


def test_template(template_name, template_func, data):
    """Test a single email template."""
    print(f"\n{'='*60}")
    print(f"Testing: {template_name}")
    print('='*60)

    try:
        result = template_func(data)
        print(f"✅ Subject: {result['subject']}")
        print(f"✅ HTML body length: {len(result['html_body'])} chars")
        print(f"✅ Text body length: {len(result.get('text_body', ''))} chars")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def send_test_email(to_email):
    """Send a test email."""
    print(f"\n{'='*60}")
    print("SENDING TEST EMAIL")
    print('='*60)
    print(f"To: {to_email}")

    # Generate test email
    data = {
        "kpi_title": "Test KPI - Email System Verification",
        "submitter_name": "System Administrator",
        "year": 2025,
        "quarter": "Q4",
        "link": "http://localhost/kpis/1"
    }

    template = kpi_submitted_email(data)

    try:
        success = email_service.send_email(
            to_emails=[to_email],
            subject=f"[TEST] {template['subject']}",
            body_html=template['html_body'],
            body_text=template.get('text_body')
        )

        if success:
            print(f"✅ Email sent successfully to {to_email}!")
            print("Check your inbox (and spam folder)")
            return True
        else:
            print("❌ Failed to send email")
            print("Check the logs for details")
            return False

    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False


def main():
    """Run email system tests."""
    print("\n" + "="*60)
    print("EMAIL NOTIFICATION SYSTEM TEST")
    print("="*60)
    print()

    # Test 1: SMTP Configuration
    if not test_smtp_connection():
        print("\n⚠️  Fix SMTP configuration before continuing")
        sys.exit(1)

    # Test 2: Email Templates
    print("\n" + "="*60)
    print("TESTING EMAIL TEMPLATES")
    print("="*60)

    templates = [
        ("KPI Submitted", kpi_submitted_email, {
            "kpi_title": "Increase Sales by 20%",
            "submitter_name": "John Doe",
            "year": 2025,
            "quarter": "Q1",
            "link": "http://localhost/kpis/1"
        }),
        ("KPI Approved", kpi_approved_email, {
            "kpi_title": "Increase Sales by 20%",
            "approver_name": "Jane Manager",
            "year": 2025,
            "quarter": "Q1",
            "link": "http://localhost/kpis/1"
        }),
        ("KPI Rejected", kpi_rejected_email, {
            "kpi_title": "Increase Sales by 20%",
            "approver_name": "Jane Manager",
            "year": 2025,
            "quarter": "Q1",
            "reason": "Target needs to be more specific",
            "link": "http://localhost/kpis/1"
        }),
        ("Comment Mention", comment_mention_email, {
            "kpi_title": "Increase Sales by 20%",
            "commenter_name": "Bob Colleague",
            "comment_text": "@john What's the current progress on this?",
            "link": "http://localhost/kpis/1"
        }),
        ("Password Reset", password_reset_email, {
            "user_name": "John Doe",
            "reset_link": "http://localhost/reset-password?token=abc123",
            "expiry_hours": 24
        }),
        ("Weekly Digest", weekly_digest_email, {
            "user_name": "John Doe",
            "period": "Oct 28 - Nov 3, 2025",
            "stats": {
                "kpis_updated": 5,
                "pending_approvals": 2,
                "new_comments": 8,
                "avg_progress": 67
            },
            "link": "http://localhost/dashboard"
        })
    ]

    all_passed = True
    for name, func, data in templates:
        if not test_template(name, func, data):
            all_passed = False

    if not all_passed:
        print("\n❌ Some template tests failed")
        sys.exit(1)

    print("\n✅ All template tests passed!")

    # Test 3: Send Test Email (optional)
    print("\n" + "="*60)
    print("SEND TEST EMAIL?")
    print("="*60)
    print("Enter an email address to send a test email, or press Enter to skip:")
    to_email = input("> ").strip()

    if to_email:
        if "@" not in to_email:
            print("❌ Invalid email address")
            sys.exit(1)

        send_test_email(to_email)
    else:
        print("Skipped test email")

    print("\n" + "="*60)
    print("✅ EMAIL SYSTEM TEST COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
