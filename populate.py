import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Project, ProjectCategory, Technology
from profiles.models import Profile, Skill, Education, Experience

def populate():
    print("Clearing old data...")
    Profile.objects.all().delete()
    Skill.objects.all().delete()
    Education.objects.all().delete()
    Experience.objects.all().delete()
    Project.objects.all().delete()
    ProjectCategory.objects.all().delete()
    Technology.objects.all().delete()

    print("Creating Profile...")
    profile = Profile.objects.create(
        name="Joseph Kiarie",
        professional_title="Full-Stack Developer",
        bio="I am a passionate Full-Stack Developer specializing in building robust, scalable web applications and delivering exceptional user experiences. With a background in Business Information Technology, I bring a unique blend of technical expertise and business acumen to every project.",
        location="Kenya",
        email="josephkiarie@example.com",
        github_url="https://github.com/joseph001technology"
    )

    print("Creating Skills...")
    skills = ['Python', 'Django', 'JavaScript', 'HTML/CSS', 'PostgreSQL', 'React', 'Git', 'REST APIs', 'Supabase']
    for idx, skill in enumerate(skills):
        Skill.objects.create(name=skill, ordering=idx)

    print("Creating Education...")
    Education.objects.create(
        institution="JKUAT (Jomo Kenyatta University of Agriculture and Technology)",
        qualification="Bachelor's Degree",
        field="Business Information Technology (BBIT)",
        start_date="2018-09-01",
        end_date="2022-11-01"
    )

    print("Creating Experience...")
    Experience.objects.create(
        role="Full-Stack Developer",
        organization="Freelance",
        start_date="2022-01-01",
        current=True,
        description="Developing custom web applications, e-commerce solutions, and business management systems for various clients. Focusing on Python/Django and modern JavaScript frameworks."
    )

    print("Creating Project Categories...")
    cat_web = ProjectCategory.objects.create(name="Web Application", slug="web-application")
    cat_management = ProjectCategory.objects.create(name="Management System", slug="management-system")

    print("Creating Technologies...")
    tech_django = Technology.objects.create(name="Django", slug="django")
    tech_python = Technology.objects.create(name="Python", slug="python")
    tech_postgres = Technology.objects.create(name="PostgreSQL", slug="postgresql")
    tech_js = Technology.objects.create(name="JavaScript", slug="javascript")

    print("Creating Projects...")
    
    # Project 1: JoseKiarie Pharmacy
    p1 = Project.objects.create(
        title="JoseKiarie Pharmacy",
        slug="josekiarie-pharmacy",
        short_description="A comprehensive stock management system for pharmacies.",
        description="JoseKiarie Pharmacy is a robust stock management system designed specifically for pharmacies. It handles inventory tracking, sales processing, supplier management, and generates detailed reports to ensure efficient pharmacy operations.",
        category=cat_management,
        status="Completed",
        featured=True,
        ordering=1,
        year=2023,
        github_url="https://github.com/joseph001technology/JoseKiarie-Pharmacy"
    )
    p1.technologies.add(tech_django, tech_python, tech_postgres, tech_js)

    # Project 2: AgriFlow
    p2 = Project.objects.create(
        title="AgriFlow",
        slug="agriflow",
        short_description="Farm product ordering application connecting farmers directly to buyers.",
        description="AgriFlow is an innovative e-commerce platform that bridges the gap between farmers and consumers. It allows farmers to list their fresh produce and enables buyers to easily order farm products, ensuring better prices for farmers and fresh produce for buyers.",
        category=cat_web,
        status="Completed",
        featured=True,
        ordering=2,
        year=2024
    )
    p2.technologies.add(tech_django, tech_python, tech_postgres)

    print("Data population completed successfully!")

if __name__ == '__main__':
    populate()
