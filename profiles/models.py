from django.db import models
from django.core.exceptions import ValidationError


class Profile(models.Model):
    name = models.CharField(max_length=150, default="Joseph Kiarie")
    headline = models.CharField(
        max_length=200,
        default="Full-Stack Developer & Systems Architect"
    )
    short_bio = models.TextField(
        help_text="Concise, impact-focused bio for hero & quick introductions."
    )
    long_bio = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed professional narrative, engineering principles, and background."
    )
    photo = models.ImageField(upload_to='profile/', blank=True, null=True)
    location = models.CharField(max_length=150, default="Nairobi, Kenya")
    
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    
    availability_status = models.CharField(
        max_length=150,
        default="Available for new client projects & technical consulting",
        help_text="Current contract/consulting availability badge"
    )
    response_time_statement = models.CharField(
        max_length=150,
        default="I typically respond within 24-48 business hours.",
        help_text="Clear turnaround expectation for prospective clients"
    )
    
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True)
    
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Profile (Site Owner)"
        verbose_name_plural = "Profile (Site Owner)"

    def clean(self):
        # Enforce singleton pattern in database
        if not self.pk and Profile.objects.exists():
            raise ValidationError("There can only be one Profile instance for the site.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} — {self.headline}"

    # Backwards compatibility properties
    @property
    def professional_title(self):
        return self.headline

    @property
    def bio(self):
        return self.short_bio

    @property
    def profile_image(self):
        return self.photo


class SocialLink(models.Model):
    PLATFORM_CHOICES = (
        ('github', 'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'X / Twitter'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('website', 'Personal / Other Website'),
    )

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, default='github')
    label = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. github.com/joseph001technology")
    url = models.URLField()
    icon = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Icon identifier (e.g. github, linkedin, twitter, whatsapp, mail, globe)"
    )
    display_order = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'platform']

    def __str__(self):
        return f"{self.get_platform_display()} ({self.url})"


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="e.g. Backend & Systems, Mobile Development, Databases & Storage, Tools & DevOps"
    )
    proficiency = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="e.g. Advanced, Production, Core Stack"
    )
    display_order = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    @property
    def ordering(self):
        return self.display_order


class Experience(models.Model):
    organisation = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Jan 2024 or 2023")
    end_date = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Leave blank if currently working here"
    )
    current = models.BooleanField(default=False)
    description = models.TextField(
        blank=True,
        null=True,
        help_text="High-level context of the role and organizational mission."
    )
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-id']

    def __str__(self):
        return f"{self.role} at {self.organisation}"


class ExperienceBullet(models.Model):
    experience = models.ForeignKey(
        Experience,
        on_delete=models.CASCADE,
        related_name='bullets'
    )
    text = models.TextField(help_text="Specific technical achievement or responsibility.")
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"Bullet for {self.experience.role}: {self.text[:50]}..."


class Education(models.Model):
    institution = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200)
    field = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.CharField(max_length=50, blank=True, null=True)
    end_date = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Present, 2025")
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Specializations, core coursework (e.g. Software Engineering, Distributed Systems)."
    )
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-id']

    def __str__(self):
        return f"{self.qualification} — {self.institution}"

    @property
    def description(self):
        return self.notes


class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date = models.CharField(max_length=50, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-id']

    def __str__(self):
        return f"{self.title} ({self.issuer})"
