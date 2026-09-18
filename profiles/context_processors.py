from .models import Profile, SocialLink

def site_profile(request):
    """
    Context processor to make the site Profile and Social Links
    globally available across all templates (nav, footer, contact links).
    """
    profile = Profile.objects.first()
    social_links = SocialLink.objects.filter(is_public=True)
    return {
        'site_profile': profile,
        'profile': profile,  # backwards compatibility
        'social_links': social_links,
    }
