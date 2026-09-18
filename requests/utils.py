import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def send_project_request_email(client_request):
    """
    Sends an email notification when a new client project request is submitted.
    Saved to database FIRST. A failed email never loses the submission.
    """
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
    
    recipient_email = getattr(settings, 'PORTFOLIO_NOTIFICATION_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None)
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'noreply@josephkiarie.dev'
    
    if recipient_email:
        try:
            send_mail(
                subject,
                body,
                from_email,
                [recipient_email],
                fail_silently=True,
            )
        except Exception as e:
            logger.warning(f"Could not dispatch project request notification email: {e}")
