import json
import logging
import os
import threading
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)

RESEND_URL = "https://api.resend.com/emails"


def _recipient():
    return (
        getattr(settings, 'PORTFOLIO_NOTIFICATION_EMAIL', '')
        or getattr(settings, 'EMAIL_HOST_USER', '')
        or ''
    ).strip()


def _send_via_resend(api_key, sender, recipient, subject, body, reply_to):
    """
    Send through Resend's HTTPS API (port 443).
    Render's free tier blocks SMTP ports (25/465/587) but not HTTPS.
    Uses only the standard library on purpose: this project has an app called
    "requests", which would shadow the PyPI "requests" package.
    """
    payload = {"from": sender, "to": [recipient], "subject": subject, "text": body}
    if reply_to:
        payload["reply_to"] = reply_to
    req = urllib.request.Request(
        RESEND_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "portfolio-site/1.0",   # Resend's firewall rejects requests without one
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        logger.info("Resend accepted notification (HTTP %s)", resp.status)


def _send_via_smtp(sender, recipient, subject, body, reply_to):
    """Fallback for hosts where SMTP is open (local machine, paid Render instance...)."""
    msg = EmailMessage(subject, body, sender, [recipient], reply_to=[reply_to] if reply_to else None)
    msg.send(fail_silently=False)


def notify_async(subject, body, reply_to=None):
    """
    Email the site owner WITHOUT ever blocking or breaking the request.

    The submission is already saved to the database before this is called, so
    a failure here can never lose a message. Sending happens in a background
    thread with short timeouts.

    Transport: RESEND_API_KEY set -> Resend HTTPS API, otherwise Django SMTP.
    Recipient: PORTFOLIO_NOTIFICATION_EMAIL (falls back to EMAIL_HOST_USER).
    """
    recipient = _recipient()
    if not recipient:
        logger.warning("Notification skipped: set PORTFOLIO_NOTIFICATION_EMAIL. (Message is saved in Django admin.)")
        return

    api_key = os.environ.get('RESEND_API_KEY', '').strip()
    if api_key:
        sender = os.environ.get('RESEND_FROM_EMAIL', '').strip() or "Portfolio <onboarding@resend.dev>"
    else:
        sender = getattr(settings, 'DEFAULT_FROM_EMAIL', '') or getattr(settings, 'EMAIL_HOST_USER', '') or 'webmaster@localhost'

    def _send():
        try:
            if api_key:
                _send_via_resend(api_key, sender, recipient, subject, body, reply_to)
            else:
                _send_via_smtp(sender, recipient, subject, body, reply_to)
        except urllib.error.HTTPError as exc:
            detail = ""
            try:
                detail = exc.read().decode("utf-8", "replace")[:300]
            except Exception:  # noqa: BLE001
                pass
            logger.warning("Notification email rejected by Resend (HTTP %s): %s", exc.code, detail)
        except Exception as exc:  # noqa: BLE001 - must never propagate
            logger.warning("Notification email failed: %s", exc)

    threading.Thread(target=_send, daemon=True).start()


def send_project_request_email(client_request):
    """Email notification for a new project request (saved to DB first)."""
    try:
        subject = f"New Project Request: {client_request.project_title or client_request.get_project_type_display() or 'General'} — {client_request.name}"
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
- Reference Project: {client_request.requested_project.title if client_request.requested_project else 'None'}
- Budget Range: {client_request.get_budget_range_display() if client_request.budget_range else 'Flexible / To be discussed'}
- Timeline: {client_request.deadline or 'Flexible'}

Project Details & Requirements:
{client_request.details}

Submitted at: {client_request.submitted_at}
View full submission in Django Admin.
"""
        notify_async(subject, body, reply_to=client_request.email)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not build project request email: %s", exc)
