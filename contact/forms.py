from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your full name',
                'required': True,
                'id': 'id_contact_name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your.email@example.com',
                'required': True,
                'id': 'id_contact_email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'What is this regarding?',
                'required': True,
                'id': 'id_contact_subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'rows': 5,
                'placeholder': 'Write your message here...',
                'required': True,
                'id': 'id_contact_message'
            }),
        }
