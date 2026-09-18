from django.db import models
from portfolio.models import Project


class ClientProjectRequest(models.Model):
    STATUS_CHOICES = (
        ('New', 'New Request'),
        ('Under Review', 'Under Review'),
        ('Contacted', 'Contacted Client'),
        ('Scoping', 'Scoping / Requirements'),
        ('Quoted', 'Quoted / Proposal Sent'),
        ('Accepted', 'Accepted & Scheduled'),
        ('Declined', 'Declined / Not Feasible'),
        ('Completed', 'Project Completed'),
    )

    PROJECT_TYPE_CHOICES = (
        ('web_system', 'Web Application / Management System (Django)'),
        ('mobile_app', 'Mobile Application (Flutter)'),
        ('api_backend', 'REST API / Backend Engineering (DRF, PostgreSQL)'),
        ('full_stack', 'End-to-End System (Web + Mobile + Cloud DB)'),
        ('consulting', 'Architecture / Database Review / Code Audit'),
        ('other', 'Other Custom Technical Solution'),
    )

    BUDGET_CHOICES = (
        ('', 'Prefer to discuss after scoping / Flexible'),
        ('tier_starter', '< 50,000 KES (~$400) — Scoped feature / prototype'),
        ('tier_medium', '50,000 – 150,000 KES (~$400 - $1,200) — Standalone system'),
        ('tier_enterprise', '150,000 – 350,000+ KES (~$1,200 - $2,800+) — Enterprise / multi-platform'),
        ('open', 'Open budget / Ongoing retainer'),
    )

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Direct phone or WhatsApp number"
    )
    organisation = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Company, enterprise, cooperative, or initiative name"
    )
    
    project_type = models.CharField(
        max_length=50,
        choices=PROJECT_TYPE_CHOICES,
        default='web_system',
        blank=True,
        null=True
    )
    requested_project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='client_requests',
        help_text="Reference project if the client liked an existing case study"
    )
    project_title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Brief working title for the initiative"
    )
    details = models.TextField(
        help_text="Describe the operational problem, core workflows, and desired outcomes."
    )
    budget_range = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        choices=BUDGET_CHOICES,
        help_text="Optional. A client is never forced to disclose a budget."
    )
    deadline = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Target launch window or urgent timeline"
    )
    contact_method = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Preferred channel: Email, Phone call, or WhatsApp"
    )
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='New')
    internal_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Internal notes for tracking project scope, quotes, and next steps."
    )
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Project Request"
        verbose_name_plural = "Project Requests"

    def __str__(self):
        org = f" ({self.organisation})" if self.organisation else ""
        return f"{self.name}{org} — {self.project_title or self.get_project_type_display()}"

    # Backward compatibility properties
    @property
    def created_at(self):
        return self.submitted_at

    @property
    def organization(self):
        return self.organisation

    @property
    def description(self):
        return self.details

    @property
    def budget(self):
        return self.budget_range

    @property
    def timeline(self):
        return self.deadline


# Alias for clean naming
ProjectRequest = ClientProjectRequest
