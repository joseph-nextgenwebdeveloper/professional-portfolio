import re

from django.db import models
from django.utils.text import slugify

# --------------------------------------------------------------------------
# Icon resolution for Technology.
# Every technology gets an icon automatically from the Simple Icons set
# (served by jsDelivr) so nothing has to be uploaded by hand. Order of
# precedence: uploaded `logo`  >  guessed from the technology name  >
# `icon_name` (treated as a Simple Icons slug, e.g. "django")  >  monogram.
# --------------------------------------------------------------------------
SIMPLE_ICONS_CDN = "https://cdn.jsdelivr.net/npm/simple-icons@13/icons/{slug}.svg"

# (phrase of words, simple-icons slug) - first match wins, so put the more
# specific phrases first.
ICON_PHRASES = (
    (("rest", "framework"), "django"),
    (("django",), "django"),
    (("flutter",), "flutter"),
    (("dart",), "dart"),
    (("postgresql",), "postgresql"),
    (("postgres",), "postgresql"),
    (("supabase",), "supabase"),
    (("python",), "python"),
    (("javascript",), "javascript"),
    (("typescript",), "typescript"),
    (("html5",), "html5"),
    (("html",), "html5"),
    (("css3",), "css3"),
    (("tailwind",), "tailwindcss"),
    (("react",), "react"),
    (("vue",), "vuedotjs"),
    (("next",), "nextdotjs"),
    (("node",), "nodedotjs"),
    (("docker",), "docker"),
    (("kubernetes",), "kubernetes"),
    (("nginx",), "nginx"),
    (("gunicorn",), "gunicorn"),
    (("github",), "github"),
    (("git",), "git"),
    (("postman",), "postman"),
    (("linux",), "linux"),
    (("jwt",), "jsonwebtokens"),
    (("redis",), "redis"),
    (("mysql",), "mysql"),
    (("sqlite",), "sqlite"),
    (("graphql",), "graphql"),
    (("firebase",), "firebase"),
    (("figma",), "figma"),
    (("cloudinary",), "cloudinary"),
    (("render",), "render"),
    (("bootstrap",), "bootstrap"),
)


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Project Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    category = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="e.g. Backend, Frontend, Mobile, Database, Cloud & DevOps, Architecture"
    )
    icon_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Identifier for custom SVG icon or badge label"
    )
    logo = models.ImageField(upload_to='technologies/', blank=True, null=True)
    display_order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # ---- icon helpers (no database columns, so no migration needed) ----
    @property
    def icon_slug(self):
        """Simple Icons slug for this technology, or '' if none is known."""
        words = re.findall(r"[a-z0-9]+", (self.name or "").lower())
        for phrase, slug in ICON_PHRASES:
            if all(w in words for w in phrase):
                return slug
        # Name not recognised: fall back to whatever is typed in icon_name
        # (older seed data has values like "api" that are not real slugs -
        # those simply fail to load and the monogram shows instead).
        return (self.icon_name or "").strip().lower()

    @property
    def icon_url(self):
        """Best available icon URL: uploaded logo, else CDN icon, else ''."""
        if self.logo:
            try:
                return self.logo.url
            except Exception:
                pass
        slug = self.icon_slug
        return SIMPLE_ICONS_CDN.format(slug=slug) if slug else ""

    @property
    def has_uploaded_logo(self):
        return bool(self.logo)

    @property
    def initials(self):
        words = re.findall(r"[A-Za-z0-9]+", self.name or "")
        return (words[0][0] if words else "?").upper()


class Service(models.Model):
    title = models.CharField(max_length=150)
    tagline = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField()
    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Icon identifier (e.g. server, mobile, database, layers, api, shield)"
    )
    image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True,
        help_text="Small illustrative image shown on the compact service card. Falls back to the icon if left blank."
    )
    deliverables = models.TextField(
        blank=True,
        null=True,
        help_text="Comma-separated or newline-separated deliverables"
    )
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'title']

    def __str__(self):
        return self.title

    def get_deliverables_list(self):
        if not self.deliverables:
            return []
        lines = [item.strip() for item in self.deliverables.replace('\r\n', '\n').split('\n') if item.strip()]
        if len(lines) == 1 and ',' in lines[0]:
            return [x.strip() for x in lines[0].split(',') if x.strip()]
        return lines


class Project(models.Model):
    STATUS_CHOICES = (
        ('Completed', 'Completed'),
        ('In Progress', 'In Progress'),
        ('Prototype', 'Prototype'),
        ('Planned', 'Planned'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    tagline = models.CharField(
        max_length=255,
        help_text="Clear, practical one-line summary of what this system does and who it serves"
    )
    short_description = models.CharField(max_length=255, blank=True, null=True)
    
    # Case study sections
    problem_statement = models.TextField(
        blank=True,
        null=True,
        help_text="What operational bottleneck, manual inefficiency, or commercial risk did this solve?"
    )
    solution = models.TextField(
        blank=True,
        null=True,
        help_text="Technical and functional breakdown of the implemented solution."
    )
    my_role = models.TextField(
        blank=True,
        null=True,
        help_text="Your exact engineering responsibilities (e.g. Backend Architecture, Database Design, Flutter App)."
    )
    architecture_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Architecture, API design, security, caching, database schema decisions."
    )
    challenges = models.TextField(
        blank=True,
        null=True,
        help_text="Real technical challenges encountered (concurrency, mobile sync, payment webhooks) and how they were resolved."
    )
    outcomes = models.TextField(
        blank=True,
        null=True,
        help_text="Real, measurable outcomes and stability milestones (leave blank if not yet tracked)."
    )
    
    # Standard metadata
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects'
    )
    technologies = models.ManyToManyField(Technology, related_name='projects', blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Completed')
    year = models.CharField(max_length=4, blank=True, null=True)
    
    featured_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    
    live_url = models.URLField(
        blank=True,
        null=True,
        help_text="Live production or staging URL. Leave empty if internal or not deployed."
    )
    repo_url = models.URLField(
        blank=True,
        null=True,
        help_text="Public repository URL. Leave empty if private or client proprietary."
    )
    documentation_url = models.URLField(blank=True, null=True)
    
    is_featured = models.BooleanField(
        default=False,
        help_text="Check to display on the primary home page featured list."
    )
    is_published = models.BooleanField(
        default=True,
        help_text="Uncheck to hide from all public pages without deleting."
    )
    display_order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.tagline:
            self.tagline = self.short_description or self.title
        if not self.short_description:
            self.short_description = self.tagline
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def featured(self):
        return self.is_featured

    @property
    def description(self):
        # Graceful fallback for backward compatibility
        return self.solution or self.short_description or self.tagline

    @description.setter
    def description(self, value):
        self.solution = value

    @property
    def github_url(self):
        return self.repo_url


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"Image for {self.project.title}"