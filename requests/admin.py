from django.contrib import admin
from .models import ClientProjectRequest


@admin.register(ClientProjectRequest)
class ClientProjectRequestAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'organisation',
        'project_type',
        'budget_range',
        'status',
        'submitted_at'
    )
    list_filter = ('status', 'project_type', 'submitted_at')
    search_fields = ('name', 'email', 'organisation', 'project_title', 'details')
    list_editable = ('status',)
    readonly_fields = ('submitted_at', 'updated_at')

    fieldsets = (
        ('Client Information', {
            'fields': ('name', 'email', 'phone', 'organisation', 'contact_method')
        }),
        ('Project Scope & Budget', {
            'fields': (
                'requested_project',
                'project_type',
                'project_title',
                'details',
                'budget_range',
                'deadline'
            )
        }),
        ('Review Status & Internal Tracking', {
            'fields': ('status', 'internal_notes', 'submitted_at', 'updated_at')
        }),
    )
