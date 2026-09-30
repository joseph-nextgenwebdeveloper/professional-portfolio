from django import forms
from .models import ContactMessage

# "What is this about?" is a pick-list instead of a free-text field: one less
# thing to type. The chosen text is saved in ContactMessage.subject as before.
# The first entry is only the placeholder (it is rejected if left selected).
TOPIC_CHOICES = [
    ("", "Select a topic"),
    ("General question", "General question"),
    ("Collaboration or job", "Collaboration or job"),
    ("Feedback", "Feedback"),
    ("I'd like to discuss a project", "I'd like to discuss a project"),
]


class ContactMessageForm(forms.ModelForm):
    subject = forms.ChoiceField(
        choices=TOPIC_CHOICES,
        label="What is this about?",
        widget=forms.Select(attrs={"class": "form-input form-select", "id": "id_contact_subject"}),
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-input", "placeholder": "Your name",
                "required": True, "id": "id_contact_name", "autocomplete": "name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input", "placeholder": "you@example.com",
                "required": True, "id": "id_contact_email", "autocomplete": "email",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-input form-textarea", "rows": 5,
                "placeholder": "What would you like to say?",
                "required": True, "id": "id_contact_message",
            }),
        }
