import logging
import threading

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def notify_async(subject, body):
    """
    Email the site owner WITHOUT ever blocking or breaking the request.

    The submission is already saved to the database before this is called.
    Sending happens in a background thread with a short SMTP timeout, so a
    blocked/slow mail server (or wrong credentials) can no longer turn a
    form submit into a 500 / worker timeout.
    """
    recipient = getattr(settings, 'PORTFOLIO_NOTIFICATION_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None)
    sender = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'noreply@josephkiarie.dev'
    if not recipient:
        return

    def _send():
        try:
            send_mail(subject, body, sender, [recipient], fail_silently=False)
        except Exception as exc:  # noqa: BLE001 - must never propagate
            logger.warning("Notification email failed: %s", exc)

    threading.Thread(target=_send, daemon=True).start()


def send_project_request_email(client_request):
    """Email notification for a new project request (saved to DB first)."""
    try:
        subject = f"New Project Request: {client_request.project_title or client_request.get_project_type_display()} — {client_request.name}"
        body = f"""
NEW CLIENT PROJECT REQUEST

From:
- Name: {client_request.name}
- Email: {client_request.email}
- Phone: {client_request.phone or 'Not provided'}
- Organisation: {client_request.organisation or 'Not provided'}
- Preferred Contact: {client_request.contact_method or 'Not specified'}

Project Scope:
- Project Type: {client_request.get_project_type_display()}
- Working Title: {client_request.project_title or 'Untitled'}
- Reference Project: {client_request.requested_project.title if client_request.requested_project else 'None'}
- Budget Range: {client_request.get_budget_range_display() if client_request.budget_range else 'Flexible / To be discussed'}
- Timeline: {client_request.deadline or 'Flexible'}

Project Details & Requirements:
{client_request.details}

Submitted at: {client_request.submitted_at}
View full submission in Django Admin.
"""
        notify_async(subject, body)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not build project request email: %s", exc)
