
import json
import logging
import os
import urllib.error
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)

# Resend's API endpoint.
# DO NOT replace this with your email address.
RESEND_URL = "https://api.resend.com/emails"


def _recipient():
    """
    Get the email address that should receive portfolio notifications.
    """
    return (
        getattr(settings, "PORTFOLIO_NOTIFICATION_EMAIL", "")
        or getattr(settings, "EMAIL_HOST_USER", "")
        or ""
    ).strip()


def _send_via_resend(api_key, sender, recipient, subject, body, reply_to=None):
    """
    Send an email through Resend's HTTPS API.

    HTTPS uses port 443, which avoids the SMTP networking problem that
    occurred on Render.
    """
    payload = {
        "from": sender,
        "to": [recipient],
        "subject": subject,
        "text": body,
    }

    if reply_to:
        payload["reply_to"] = [reply_to]

    request = urllib.request.Request(
        RESEND_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "portfolio-site/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            logger.info(
                "Resend accepted notification email. HTTP status: %s",
                response.status,
            )

    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8", "replace")[:500]
        except Exception:
            detail = "Unable to read Resend error response."

        logger.warning(
            "Resend rejected notification email. HTTP %s: %s",
            exc.code,
            detail,
        )

    except urllib.error.URLError as exc:
        logger.warning(
            "Could not connect to Resend: %s",
            exc,
        )

    except Exception as exc:
        logger.warning(
            "Unexpected Resend email error: %s",
            exc,
        )


def notify_async(subject, body, reply_to=None):
    """
    Send a portfolio notification email.

    The form submission is saved to the database before this function
    is called. Therefore, an email failure will not prevent the user's
    submission from being saved.
    """
    recipient = _recipient()

    if not recipient:
        logger.warning(
            "Notification skipped: set PORTFOLIO_NOTIFICATION_EMAIL. "
            "(Message is saved in Django admin.)"
        )
        return

    api_key = os.environ.get("RESEND_API_KEY", "").strip()

    if not api_key:
        logger.warning(
            "Notification skipped: RESEND_API_KEY is not configured."
        )
        return

    sender = (
        os.environ.get("RESEND_FROM_EMAIL", "").strip()
        or "Portfolio <onboarding@resend.dev>"
    )

    _send_via_resend(
        api_key=api_key,
        sender=sender,
        recipient=recipient,
        subject=subject,
        body=body,
        reply_to=reply_to,
    )


def send_project_request_email(client_request):
    """
    Send an email notification when a new project request is submitted.
    """
    try:
        project_name = (
            client_request.project_title
            or client_request.get_project_type_display()
            or "General"
        )

        reference_project = "None"

        if client_request.requested_project:
            reference_project = client_request.requested_project.title

        budget_range = "Flexible / To be discussed"

        if client_request.budget_range:
            budget_range = client_request.get_budget_range_display()

        subject = (
            f"New Project Request: "
            f"{project_name} — {client_request.name}"
        )

        body = f"""
NEW CLIENT PROJECT REQUEST

From:
- Name: {client_request.name}
- Email: {client_request.email}
- Phone: {client_request.phone or 'Not provided'}
- Organisation: {client_request.organisation or 'Not provided'}
- Preferred Contact: {client_request.contact_method or 'Not specified'}

Project Scope:
- Project Type: {client_request.get_project_type_display() or 'Not specified'}
- Working Title: {client_request.project_title or 'Untitled'}
- Reference Project: {reference_project}
- Budget Range: {budget_range}
- Timeline: {client_request.deadline or 'Flexible'}

Project Details & Requirements:
{client_request.details}

Submitted at:
{client_request.submitted_at}

View the full submission in Django Admin.
"""

        notify_async(
            subject=subject,
            body=body,
            reply_to=client_request.email,
        )

    except Exception as exc:
        logger.warning(
            "Could not build project request email: %s",
            exc,
        )

