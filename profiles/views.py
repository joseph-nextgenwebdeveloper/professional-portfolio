from django.shortcuts import render
from .models import Profile, Skill, Education, Experience, Certification, SocialLink


def about(request):
    """
    Detailed about page:
    Narrative, engineering background, skills breakdown by category,
    experience with bullet achievements, education, and social channels.
    """
    profile = Profile.objects.first()
    skills = Skill.objects.filter(active=True).order_by('display_order', 'name')
    education = Education.objects.all().order_by('display_order', '-id')
    experience = Experience.objects.all().prefetch_related('bullets').order_by('display_order', '-id')
    certifications = Certification.objects.all().order_by('display_order', '-id')
    social_links = SocialLink.objects.filter(is_public=True).order_by('display_order')
    
    # Group skills by category for clear editorial presentation
    skills_by_category = {}
    for skill in skills:
        cat = skill.category or "General Stack"
        if cat not in skills_by_category:
            skills_by_category[cat] = []
        skills_by_category[cat].append(skill)
    
    context = {
        'profile': profile,
        'skills': skills,
        'skills_by_category': skills_by_category,
        'education': education,
        'experience': experience,
        'certifications': certifications,
        'social_links': social_links,
    }
    return render(request, 'profiles/about.html', context)
