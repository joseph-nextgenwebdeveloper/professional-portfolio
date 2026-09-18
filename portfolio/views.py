from django.shortcuts import render, get_object_or_404
from .models import Project, ProjectCategory, Technology, Service
from profiles.models import Profile, Skill, Experience, Education, SocialLink


def home(request):
    """
    Primary landing page. Art-directed, section-by-section breakdown:
    1. Hero (Profile snapshot, availability, primary CTA)
    2. Technology Marquee (Restrained horizontal ticker)
    3. Featured / Selected Projects (Case-study summary cards)
    4. What I Build (Services)
    5. Skills / Core Stack
    6. About snapshot
    7. Experience & Education snapshot
    8. Project CTA band
    9. Footer
    """
    profile = Profile.objects.first()
    
    # Selected / featured projects (only published)
    featured_projects = Project.objects.filter(
        is_published=True,
        is_featured=True
    ).order_by('display_order', '-created_at')[:4]
    
    if not featured_projects.exists():
        featured_projects = Project.objects.filter(
            is_published=True
        ).order_by('display_order', '-created_at')[:4]

    # Marquee & stack
    technologies = Technology.objects.filter(active=True).order_by('display_order', 'name')
    skills = Skill.objects.filter(active=True).order_by('display_order', 'name')
    
    # Services
    services = Service.objects.filter(is_active=True).order_by('display_order')
    
    # Experience & Education snapshot
    experiences = Experience.objects.all().prefetch_related('bullets').order_by('display_order', '-id')
    educations = Education.objects.all().order_by('display_order', '-id')
    
    social_links = SocialLink.objects.filter(is_public=True).order_by('display_order')

    context = {
        'profile': profile,
        'projects': featured_projects,
        'featured_projects': featured_projects,
        'technologies': technologies,
        'skills': skills,
        'services': services,
        'experiences': experiences,
        'educations': educations,
        'social_links': social_links,
    }
    return render(request, 'portfolio/home.html', context)


def project_list(request):
    """
    Filterable projects index. Supports category and technology filtering via query params.
    Only displays published projects.
    """
    category_slug = request.GET.get('category')
    tech_slug = request.GET.get('tech')
    
    projects = Project.objects.filter(is_published=True)
    
    selected_category = None
    selected_tech = None
    
    if category_slug:
        selected_category = get_object_or_404(ProjectCategory, slug=category_slug)
        projects = projects.filter(category=selected_category)
        
    if tech_slug:
        selected_tech = get_object_or_404(Technology, slug=tech_slug)
        projects = projects.filter(technologies=selected_tech)
        
    projects = projects.distinct().order_by('display_order', '-created_at')
    
    categories = ProjectCategory.objects.filter(active=True)
    technologies = Technology.objects.filter(active=True)

    context = {
        'projects': projects,
        'categories': categories,
        'technologies': technologies,
        'selected_category': selected_category,
        'selected_tech': selected_tech,
    }
    return render(request, 'portfolio/project_list.html', context)


def project_detail(request, slug):
    """
    Case-study detail view:
    Problem, Solution, Architecture, Technologies, Role, Challenges, Outcomes, Gallery, Links.
    """
    project = get_object_or_404(Project, slug=slug, is_published=True)
    other_projects = Project.objects.filter(
        is_published=True
    ).exclude(id=project.id).order_by('display_order')[:3]

    context = {
        'project': project,
        'other_projects': other_projects,
    }
    return render(request, 'portfolio/project_detail.html', context)
