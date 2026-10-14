from django import forms
from .models import ClientProjectRequest
from portfolio.models import Project


class ClientProjectRequestForm(forms.ModelForm):
    budget_range = forms.ChoiceField(
        choices=ClientProjectRequest.BUDGET_CHOICES,
        required=False,
        initial='',
        widget=forms.RadioSelect,
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

    # Friendly labels; the stored keys are unchanged so old data and admin still work.
    project_type = forms.ChoiceField(
        required=False,
        label="What do you need?",
        choices=(
            ('web_system', 'Website or web app'),
            ('mobile_app', 'Mobile app'),
            ('api_backend', 'Backend / API'),
            ('full_stack', 'Web + mobile system'),
            ('consulting', 'Review or advice'),
            ('other', 'Something else'),
        ),
        widget=forms.RadioSelect,
    )

    class Meta:
        model = ClientProjectRequest
        # Kept short on purpose. Organisation, working title and preferred
        # channel were dropped from the form (the columns still exist).
        fields = ['name', 'email', 'project_type', 'requested_project', 'details', 'phone', 'budget_range', 'deadline']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your name', 'required': True, 'id': 'id_name', 'autocomplete': 'name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'you@example.com', 'required': True, 'id': 'id_email', 'autocomplete': 'email'}),
            'requested_project': forms.HiddenInput(),
            'details': forms.Textarea(attrs={'class': 'form-input form-textarea', 'rows': 5, 'required': True, 'id': 'id_details',
                        'placeholder': 'What problem are you trying to solve? A few lines is plenty.'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone / WhatsApp', 'id': 'id_phone'}),
            'deadline': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. within 2 months', 'id': 'id_deadline'}),
        }
