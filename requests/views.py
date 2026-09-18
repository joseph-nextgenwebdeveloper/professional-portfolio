from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
            return redirect('portfolio:home')
    else:
        form = ClientProjectRequestForm(initial=initial_data)
        
    context = {
        'form': form,
        'requested_project': requested_project,
    }
    return render(request, 'requests/request_form.html', context)
