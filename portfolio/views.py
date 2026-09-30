from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Project, ProjectCategory, Technology, Service
from profiles.models import Profile, Experience, Education, Certification

# How many projects the one-page home shows before "View all projects".
HOME_PROJECT_LIMIT = 4


def _projects_qs():
    """Published projects with everything the cards + popups need, in 3 queries."""
    return (
        Project.objects.filter(is_published=True)
        .select_related('category')
        .prefetch_related('technologies', 'images')
    )


def home(request):
    """
    The whole portfolio on one page, in this order:
    Hero -> Marquee -> About -> Experience -> Projects -> Services -> Stack -> CTA.
    Project details open in a popup, so there is no separate detail page.
    """
    profile = Profile.objects.first()

    featured = _projects_qs().filter(is_featured=True).order_by('display_order', '-created_at')[:HOME_PROJECT_LIMIT]
    featured = list(featured)
    if not featured:
        featured = list(_projects_qs().order_by('display_order', '-created_at')[:HOME_PROJECT_LIMIT])

    total_projects = Project.objects.filter(is_published=True).count()

    # ONE list of technologies (the old separate "Skills" list was removed).
    technologies = list(Technology.objects.filter(active=True).order_by('display_order', 'name'))

    context = {
        'profile': profile,
        'featured_projects': featured,
        'total_projects': total_projects,
        'has_more_projects': total_projects > len(featured),
        'technologies': technologies,
        'marquee_technologies': technologies[:10],
        'services': Service.objects.filter(is_active=True).order_by('display_order'),
        'experiences': Experience.objects.prefetch_related('bullets').order_by('display_order', '-id'),
        'educations': Education.objects.order_by('display_order', '-id'),
        'certifications': Certification.objects.order_by('display_order', '-id'),
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
