from django.urls import path
from . import views

app_name = 'requests'
urlpatterns = [
    path('request-project/', views.request_project, name='request_project'),
    path('request-project/<slug:project_slug>/', views.request_project, name='request_project_with_ref'),
]
