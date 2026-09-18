from django import forms
from .models import ClientProjectRequest
from portfolio.models import Project


class ClientProjectRequestForm(forms.ModelForm):
    budget_range = forms.ChoiceField(
        choices=ClientProjectRequest.BUDGET_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-input form-select',
            'id': 'id_budget_range'
        })
    )

    def __init__(self, *args, **kwargs):
        if len(args) > 0 and args[0] is not None:
            data = args[0].copy()
            if 'description' in data and 'details' not in data:
                data['details'] = data['description']
            if 'organization' in data and 'organisation' not in data:
                data['organisation'] = data['organization']
            args = (data,) + args[1:]
        elif 'data' in kwargs and kwargs['data']:
            data = kwargs['data'].copy()
            if 'description' in data and 'details' not in data:
                data['details'] = data['description']
            if 'organization' in data and 'organisation' not in data:
                data['organisation'] = data['organization']
            kwargs['data'] = data
        super().__init__(*args, **kwargs)

    class Meta:
        model = ClientProjectRequest
        fields = [
            'name',
            'email',
            'phone',
            'organisation',
            'project_type',
            'requested_project',
            'project_title',
            'details',
            'budget_range',
            'deadline',
            'contact_method',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your full name or title',
                'required': True,
                'id': 'id_name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'work.email@company.com',
                'required': True,
                'id': 'id_email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+254 7XX XXX XXX (for quick consultation)',
                'id': 'id_phone'
            }),
            'organisation': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Company, NGO, enterprise, or startup',
                'id': 'id_organisation'
            }),
            'project_type': forms.Select(attrs={
                'class': 'form-input form-select',
                'id': 'id_project_type'
            }),
            'requested_project': forms.Select(attrs={
                'class': 'form-input form-select',
                'id': 'id_requested_project'
            }),
            'project_title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Cooperative Logistics System or Mobile Inventory Portal',
                'id': 'id_project_title'
            }),
            'details': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'rows': 5,
                'placeholder': 'Describe what you are looking to build: existing bottlenecks, core user workflows, expected platform (Web/Mobile), or integration requirements.',
                'required': True,
                'id': 'id_details'
            }),
            'deadline': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Within 1 month, Q3 rollout, or Flexible',
                'id': 'id_deadline'
            }),
            'contact_method': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. WhatsApp, Email, or Google Meet',
                'id': 'id_contact_method'
            }),
        }
