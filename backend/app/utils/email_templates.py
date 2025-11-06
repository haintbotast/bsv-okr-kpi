"""Email templates for notifications."""

from typing import Dict, Any
from app.config import settings


def get_base_template(content: str) -> str:
    """
    Get base HTML template for emails.

    Args:
        content: HTML content to insert into template

    Returns:
        Complete HTML email template
    """
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px 20px;
            text-align: center;
            color: #ffffff;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            font-weight: 600;
        }}
        .content {{
            padding: 30px 20px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 24px;
            margin: 20px 0;
            background-color: #667eea;
            color: #ffffff;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 500;
        }}
        .button:hover {{
            background-color: #5568d3;
        }}
        .info-box {{
            background-color: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #666;
        }}
        .label {{
            font-weight: 600;
            color: #667eea;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{settings.APP_NAME}</h1>
        </div>
        <div class="content">
            {content}
        </div>
        <div class="footer">
            <p>This is an automated message from {settings.APP_NAME}.</p>
            <p>Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
"""


def kpi_submitted_email(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Email template for KPI submission notification.

    Args:
        data: Dict containing kpi_title, submitter_name, year, quarter, link

    Returns:
        Dict with subject, html_body, text_body
    """
    content = f"""
        <h2>New KPI Submitted for Approval</h2>
        <p>A new KPI has been submitted and requires your approval.</p>

        <div class="info-box">
            <p><span class="label">KPI:</span> {data['kpi_title']}</p>
            <p><span class="label">Submitted by:</span> {data['submitter_name']}</p>
            <p><span class="label">Period:</span> {data['year']} {data['quarter']}</p>
        </p>
        </div>

        <p>
            <a href="{data['link']}" class="button">Review KPI</a>
        </p>

        <p>Please review and approve or reject this KPI at your earliest convenience.</p>
    """

    text_body = f"""
New KPI Submitted for Approval

A new KPI has been submitted and requires your approval.

KPI: {data['kpi_title']}
Submitted by: {data['submitter_name']}
Period: {data['year']} {data['quarter']}

Review KPI: {data['link']}

Please review and approve or reject this KPI at your earliest convenience.
"""

    return {
        "subject": f"KPI Submitted for Approval: {data['kpi_title']}",
        "html_body": get_base_template(content),
        "text_body": text_body
    }


def kpi_approved_email(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Email template for KPI approval notification.

    Args:
        data: Dict containing kpi_title, approver_name, year, quarter, link

    Returns:
        Dict with subject, html_body, text_body
    """
    content = f"""
        <h2>✅ Your KPI Has Been Approved!</h2>
        <p>Congratulations! Your KPI has been approved.</p>

        <div class="info-box">
            <p><span class="label">KPI:</span> {data['kpi_title']}</p>
            <p><span class="label">Approved by:</span> {data['approver_name']}</p>
            <p><span class="label">Period:</span> {data['year']} {data['quarter']}</p>
        </div>

        <p>
            <a href="{data['link']}" class="button">View KPI</a>
        </p>

        <p>You can now track progress and update your KPI.</p>
    """

    text_body = f"""
✅ Your KPI Has Been Approved!

Congratulations! Your KPI has been approved.

KPI: {data['kpi_title']}
Approved by: {data['approver_name']}
Period: {data['year']} {data['quarter']}

View KPI: {data['link']}

You can now track progress and update your KPI.
"""

    return {
        "subject": f"KPI Approved: {data['kpi_title']}",
        "html_body": get_base_template(content),
        "text_body": text_body
    }


def kpi_rejected_email(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Email template for KPI rejection notification.

    Args:
        data: Dict containing kpi_title, approver_name, year, quarter, reason, link

    Returns:
        Dict with subject, html_body, text_body
    """
    content = f"""
        <h2>❌ Your KPI Has Been Rejected</h2>
        <p>Your KPI has been reviewed and requires changes before approval.</p>

        <div class="info-box">
            <p><span class="label">KPI:</span> {data['kpi_title']}</p>
            <p><span class="label">Reviewed by:</span> {data['approver_name']}</p>
            <p><span class="label">Period:</span> {data['year']} {data['quarter']}</p>
            <p><span class="label">Reason:</span> {data.get('reason', 'No reason provided')}</p>
        </div>

        <p>
            <a href="{data['link']}" class="button">Edit KPI</a>
        </p>

        <p>Please address the feedback and resubmit your KPI for approval.</p>
    """

    text_body = f"""
❌ Your KPI Has Been Rejected

Your KPI has been reviewed and requires changes before approval.

KPI: {data['kpi_title']}
Reviewed by: {data['approver_name']}
Period: {data['year']} {data['quarter']}
Reason: {data.get('reason', 'No reason provided')}

Edit KPI: {data['link']}

Please address the feedback and resubmit your KPI for approval.
"""

    return {
        "subject": f"KPI Requires Changes: {data['kpi_title']}",
        "html_body": get_base_template(content),
        "text_body": text_body
    }


def comment_mention_email(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Email template for comment mention notification.

    Args:
        data: Dict containing kpi_title, commenter_name, comment_text, link

    Returns:
        Dict with subject, html_body, text_body
    """
    content = f"""
        <h2>💬 You Were Mentioned in a Comment</h2>
        <p>You were mentioned in a comment on a KPI.</p>

        <div class="info-box">
            <p><span class="label">KPI:</span> {data['kpi_title']}</p>
            <p><span class="label">Comment by:</span> {data['commenter_name']}</p>
            <p><span class="label">Comment:</span></p>
            <p style="margin-left: 15px; font-style: italic;">"{data['comment_text']}"</p>
        </div>

        <p>
            <a href="{data['link']}" class="button">View Comment</a>
        </p>
    """

    text_body = f"""
💬 You Were Mentioned in a Comment

You were mentioned in a comment on a KPI.

KPI: {data['kpi_title']}
Comment by: {data['commenter_name']}
Comment: "{data['comment_text']}"

View Comment: {data['link']}
"""

    return {
        "subject": f"You were mentioned in a comment on: {data['kpi_title']}",
        "html_body": get_base_template(content),
        "text_body": text_body
    }


def password_reset_email(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Email template for password reset.

    Args:
        data: Dict containing user_name, reset_link, expiry_hours

    Returns:
        Dict with subject, html_body, text_body
    """
    content = f"""
        <h2>🔐 Password Reset Request</h2>
        <p>Hello {data['user_name']},</p>
        <p>We received a request to reset your password. Click the button below to create a new password:</p>

        <p>
            <a href="{data['reset_link']}" class="button">Reset Password</a>
        </p>

        <div class="info-box">
            <p><strong>⚠️ Security Notice:</strong></p>
            <p>This link will expire in {data.get('expiry_hours', 24)} hours.</p>
            <p>If you didn't request a password reset, please ignore this email or contact your administrator.</p>
        </div>

        <p>For security reasons, please do not share this link with anyone.</p>
    """

    text_body = f"""
🔐 Password Reset Request

Hello {data['user_name']},

We received a request to reset your password. Click the link below to create a new password:

{data['reset_link']}

⚠️ Security Notice:
- This link will expire in {data.get('expiry_hours', 24)} hours.
- If you didn't request a password reset, please ignore this email or contact your administrator.

For security reasons, please do not share this link with anyone.
"""

    return {
        "subject": "Password Reset Request - " + settings.APP_NAME,
        "html_body": get_base_template(content),
        "text_body": text_body
    }


def weekly_digest_email(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Email template for weekly activity digest.

    Args:
        data: Dict containing user_name, period, stats, link

    Returns:
        Dict with subject, html_body, text_body
    """
    stats = data.get('stats', {})

    content = f"""
        <h2>📊 Your Weekly Digest</h2>
        <p>Hello {data['user_name']},</p>
        <p>Here's your activity summary for {data['period']}:</p>

        <div class="info-box">
            <p><span class="label">KPIs Updated:</span> {stats.get('kpis_updated', 0)}</p>
            <p><span class="label">Pending Approvals:</span> {stats.get('pending_approvals', 0)}</p>
            <p><span class="label">New Comments:</span> {stats.get('new_comments', 0)}</p>
            <p><span class="label">Average Progress:</span> {stats.get('avg_progress', 0)}%</p>
        </div>

        <p>
            <a href="{data['link']}" class="button">View Dashboard</a>
        </p>
    """

    text_body = f"""
📊 Your Weekly Digest

Hello {data['user_name']},

Here's your activity summary for {data['period']}:

- KPIs Updated: {stats.get('kpis_updated', 0)}
- Pending Approvals: {stats.get('pending_approvals', 0)}
- New Comments: {stats.get('new_comments', 0)}
- Average Progress: {stats.get('avg_progress', 0)}%

View Dashboard: {data['link']}
"""

    return {
        "subject": f"Your Weekly Digest - {data['period']}",
        "html_body": get_base_template(content),
        "text_body": text_body
    }
