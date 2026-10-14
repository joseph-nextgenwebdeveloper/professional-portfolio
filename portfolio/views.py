import os
import re

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .models import Project, ProjectCategory, Technology, Service
from profiles.models import Profile, Experience, Education, Certification
from contact.forms import ContactMessageForm
from requests.forms import ClientProjectRequestForm

# Most projects the home page shows (cards get smaller as the count grows).
# Everything beyond this is one click away on the archive page.
HOME_PROJECT_LIMIT = 10


def grid_size(count):
    """Card-size tier: the more projects, the smaller the boxes."""
    if count <= 4:
        return 'l'
    if count <= 6:
        return 'm'
    if count <= 8:
        return 's'
    return 'xs'


def _projects_qs():
    """Published projects with everything the cards + popups need, in 3 queries."""
    return (
        Project.objects.filter(is_published=True)
        .select_related('category')
        .prefetch_related('technologies', 'images')
    )


def whatsapp_number(profile):
    """
    Digits-only international number for wa.me links (e.g. 2547XXXXXXXX).
    Uses the WHATSAPP_NUMBER env var, else the phone saved on the Profile.
    A leading 0 or a bare 9-digit Kenyan number is converted to 254...
    """
    raw = os.environ.get('WHATSAPP_NUMBER', '') or (getattr(profile, 'phone', '') or '')
    digits = re.sub(r'\D', '', raw)
    if digits.startswith('00'):
        digits = digits[2:]
    if digits.startswith('0'):
        digits = '254' + digits[1:]
    elif len(digits) == 9 and digits[0] in '17':
        digits = '254' + digits
    return digits


def home(request, contact_form=None, request_form=None, active_tab=None):
    """
    The whole portfolio on one page, in this order:
    Hero -> Marquee -> About -> Experience -> Projects -> Services -> Stack -> Contact / Request.
    Project details open in a popup, so there is no separate detail page.

    contact_form / request_form / active_tab are passed in by the contact and
    request views when a form submitted from this page has errors, so the
    errors show in place instead of sending the visitor to another page.
    """
    profile = Profile.objects.first()

    # Featured projects first, then the rest, up to the limit.
    featured = list(_projects_qs().order_by('-is_featured', 'display_order', '-created_at')[:HOME_PROJECT_LIMIT])

    total_projects = Project.objects.filter(is_published=True).count()

    # ONE list of technologies (the old separate "Skills" list was removed).
    technologies = list(Technology.objects.filter(active=True).order_by('display_order', 'name'))

    context = {
        'profile': profile,
        'featured_projects': featured,
        'grid_size': grid_size(len(featured)),
        'total_projects': total_projects,
        'has_more_projects': total_projects > len(featured),
        'technologies': technologies,
        'marquee_technologies': technologies[:10],
        'services': Service.objects.filter(is_active=True).order_by('display_order'),
        'experiences': Experience.objects.prefetch_related('bullets').order_by('display_order', '-id'),
        'educations': Education.objects.order_by('display_order', '-id'),
        'certifications': Certification.objects.order_by('display_order', '-id'),
        'contact_form': contact_form or ContactMessageForm(),
        'request_form': request_form or ClientProjectRequestForm(),
        'connect_active': active_tab or 'contact',
        'whatsapp_number': whatsapp_number(profile),
    }
    return render(request, 'portfolio/home.html', context)


def project_list(request):
    """
    Full project archive (linked from "View all projects").
    Filter by category via ?category=<slug>. Cards open the same popup as the home page.
    """
    category_slug = request.GET.get('category')
    projects = _projects_qs()

    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(ProjectCategory, slug=category_slug)
        projects = projects.filter(category=selected_category)

    projects = projects.order_by('display_order', '-created_at')

    context = {
        'projects': projects,
        'grid_size': 's',
        'categories': ProjectCategory.objects.filter(active=True),
        'selected_category': selected_category,
    }
    return render(request, 'portfolio/project_list.html', context)


def project_detail(request, slug):
    """
    There is no standalone detail page any more - details live in a popup.
    Old links (/projects/<slug>/) land on the projects section and the popup opens by itself.
    """
    project = get_object_or_404(Project, slug=slug, is_published=True)
    return redirect(f"{reverse('portfolio:project_list')}#project-{project.slug}")


@require_http_methods(["GET", "HEAD"])
def health(request):
    """Lightweight keep-alive endpoint for the external cron ping: no DB, no template, tiny body."""
    return HttpResponse('{"status":"ok"}', content_type="application/json")