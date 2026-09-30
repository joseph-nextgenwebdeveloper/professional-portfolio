from django.contrib import admin
from .models import (
    Profile,
    SocialLink,
    Experience,
    ExperienceBullet,
    Education,
    Certification
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'headline', 'location', 'email', 'phone', 'availability_status')
    search_fields = ('name', 'headline', 'short_bio', 'long_bio')

    fieldsets = (
        ('Personal & Branding', {
            'fields': ('name', 'headline', 'short_bio', 'long_bio', 'photo', 'secondary_photo', 'cv_file')
        }),
        ('Location & Contact', {
            'fields': ('location', 'email', 'phone', 'github_url', 'linkedin_url')
        }),
        ('Client Availability & Turnaround', {
            'fields': ('availability_status', 'response_time_statement')
        }),
    )

    def has_add_permission(self, request):
        # Prevent multiple Profiles if one already exists
        if Profile.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'label', 'url', 'display_order', 'is_public')
    list_editable = ('display_order', 'is_public')
    list_filter = ('platform', 'is_public')
    search_fields = ('platform', 'label', 'url')


class ExperienceBulletInline(admin.TabularInline):
    model = ExperienceBullet
    extra = 2
    fields = ('text', 'display_order')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'organisation', 'start_date', 'end_date', 'current', 'display_order')
    list_filter = ('current',)
    list_editable = ('display_order', 'current')
    search_fields = ('role', 'organisation', 'description')
    inlines = [ExperienceBulletInline]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('qualification', 'institution', 'start_date', 'end_date', 'display_order')
    list_editable = ('display_order',)
    search_fields = ('qualification', 'institution', 'notes')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'date', 'url', 'display_order')
    list_editable = ('display_order',)
    search_fields = ('title', 'issuer')
