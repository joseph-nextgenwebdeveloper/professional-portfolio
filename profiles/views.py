from django.http import FileResponse, Http404
from django.shortcuts import redirect
from django.views.generic import RedirectView

from .models import Profile


class AboutRedirect(RedirectView):
    url = '/#about'
    permanent = True


def download_cv(request):
    """
    /cv/ - always downloads the CV, whatever storage it lives on.
    The plain `download` attribute is ignored by browsers for cross-origin
    links (Cloudinary), so we send them through here instead.
    """
    profile = Profile.objects.first()
    if not profile or not profile.cv_file:
        raise Http404("No CV uploaded yet.")

    url = profile.cv_file.url
    if 'res.cloudinary.com' in url:
        # fl_attachment makes Cloudinary send Content-Disposition: attachment
        if '/fl_attachment' not in url:
            url = url.replace('/upload/', '/upload/fl_attachment/', 1)
        return redirect(url)

    filename = profile.cv_file.name.rsplit('/', 1)[-1]
    return FileResponse(profile.cv_file.open('rb'), as_attachment=True, filename=filename)
