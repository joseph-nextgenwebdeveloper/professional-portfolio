from django.contrib import admin
from .models import ProjectCategory, Technology, Project, ProjectImage, Service


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('active',)
    search_fields = ('name', 'description')


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'icon_name', 'display_order', 'active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'active')
    list_editable = ('display_order', 'active')
    search_fields = ('name', 'category')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'tagline', 'icon', 'display_order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('display_order', 'is_active')
    search_fields = ('title', 'tagline', 'description')


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ('image', 'caption', 'display_order')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'status',
        'year',
        'is_featured',
        'is_published',
        'display_order',
        'created_at'
    )
    list_filter = ('is_published', 'is_featured', 'status', 'category', 'year')
    search_fields = ('title', 'tagline', 'problem_statement', 'solution', 'architecture_notes')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    filter_horizontal = ('technologies',)
    list_editable = ('is_featured', 'is_published', 'display_order', 'status')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Overview & Publishing', {
            'fields': (
                'title', 'slug', 'tagline', 'category', 'technologies',
                'status', 'year', 'is_featured', 'is_published', 'display_order'
            )
        }),
        ('Visuals & Links', {
            'fields': ('featured_image', 'live_url', 'repo_url', 'documentation_url')
        }),
        ('Case Study Details', {
            'fields': (
                'my_role',
                'problem_statement',
                'solution',
                'architecture_notes',
                'challenges',
                'outcomes'
            )
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )
