from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'is_read', 'submitted_at')
    list_filter = ('is_read', 'status', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('status', 'is_read')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)
