from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    
    path('about/', views.AboutRedirect.as_view(), name='about'),
    path('cv/', views.download_cv, name='cv'),
]
