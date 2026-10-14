from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .forms import ClientProjectRequestForm
from .utils import send_project_request_email
from portfolio.models import Project

def request_project(request, project_slug=None):
    initial_data = {}
    requested_project = None
    
    if project_slug:
        requested_project = get_object_or_404(Project, slug=project_slug)
        initial_data['requested_project'] = requested_project

    if request.method == 'POST':
        form = ClientProjectRequestForm(request.POST)
        if form.is_valid():
            client_request = form.save()
            # Send email notification
            send_project_request_email(client_request)
            messages.success(request, 'Your project request has been submitted successfully. We will get back to you soon.')
            if request.POST.get('from_home'):
                return redirect(reverse('portfolio:home') + '#connect-request')
            return redirect('portfolio:home')
        if request.POST.get('from_home'):
            # errors show inside the home page's request form
            from portfolio.views import home
            return home(request, request_form=form, active_tab='request')
    else:
        form = ClientProjectRequestForm(initial=initial_data)
        
    context = {
        'form': form,
        'requested_project': requested_project,
    }
    return render(request, 'requests/request_form.html', context)
