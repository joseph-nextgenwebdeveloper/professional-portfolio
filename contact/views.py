import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactMessageForm
from profiles.models import Profile, SocialLink

logger = logging.getLogger(__name__)


def contact(request):
    profile = Profile.objects.first()
    social_links = SocialLink.objects.filter(is_public=True)
    
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            # 1. ALWAYS SAVE TO DATABASE FIRST
            contact_msg = form.save()
            
            # 2. ATTEMPT EMAIL NOTIFICATION (FAILURE NEVER LOSES SUBMISSION)
            recipient_email = getattr(settings, 'PORTFOLIO_NOTIFICATION_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None)
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or 'noreply@josephkiarie.dev'
            
            if recipient_email:
                try:
                    send_mail(
                        subject=f"Portfolio Contact: {contact_msg.subject} from {contact_msg.name}",
                        message=f"Name: {contact_msg.name}\nEmail: {contact_msg.email}\nSubject: {contact_msg.subject}\n\nMessage:\n{contact_msg.message}\n\nSubmitted at: {contact_msg.submitted_at}",
                        from_email=from_email,
                        recipient_list=[recipient_email],
                        fail_silently=True,
                    )
                except Exception as e:
                    logger.warning(f"Could not dispatch contact email notification: {e}")

            messages.success(request, 'Your message has been received! I will get back to you shortly.')
            return redirect('contact:contact')
    else:
        form = ContactMessageForm()
        
    context = {
        'form': form,
        'profile': profile,
        'social_links': social_links,
    }
    return render(request, 'contact/contact_form.html', context)
