from django.views.generic import RedirectView


class AboutRedirect(RedirectView):
    url = '/#about'
    permanent = True
