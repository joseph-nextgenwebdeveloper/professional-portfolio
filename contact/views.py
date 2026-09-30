import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactMessageForm
from profiles.models import Profile, SocialLink
from requests.utils import notify_async

logger = logging.getLogger(__name__)


def contact(request):
    profile = Profile.objects.first()
    social_links = SocialLink.objects.filter(is_public=True)
    
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            # 1. ALWAYS SAVE TO DATABASE FIRST
            contact_msg = form.save()
            
            # 2. Email the owner in the background - can never block or break the request
            notify_async(
                subject=f"Portfolio Contact: {contact_msg.subject} from {contact_msg.name}",
                body=(
                    f"Name: {contact_msg.name}\nEmail: {contact_msg.email}\n"
                    f"Subject: {contact_msg.subject}\n\nMessage:\n{contact_msg.message}\n\n"
                    f"Submitted at: {contact_msg.submitted_at}"
                ),
            )

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
