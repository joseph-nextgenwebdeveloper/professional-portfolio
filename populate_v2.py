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
        name="Joseph Ngigi Kiarie",
        professional_title="Full-Stack Developer",
        bio="Motivated Information Technology student with a passion for building clean, functional software — from full-stack web apps to cross-platform mobile applications.\n\nAs a BBIT student, I combine technical expertise with business knowledge in marketing, accounting, and human resource management, enabling me to develop solutions that are both innovative and strategically aligned with business goals.\n\nI'm currently pursuing a Bachelor of Business Information Technology (BBIT) at JKUAT. Over the past year I've built and deployed real-world projects using Python & Django, Flutter, HTML/CSS/JS, and PostgreSQL. I believe in learning by doing — every project is a chance to push my skills further.",
        location="Nairobi, KE",
        email="josephkiarie@example.com",
        github_url="https://github.com/joseph001technology"
    )

    print("Creating Skills...")
    skills = [
        ('Frontend', 'HTML', 90),
        ('Frontend', 'CSS', 85),
        ('Frontend', 'JavaScript', 75),
        ('Frontend', 'Flutter / Dart', 85),
        ('Backend', 'Python', 90),
        ('Backend', 'Django', 95),
        ('Backend', 'REST APIs', 85),
        ('Backend', 'JWT Auth', 80),
        ('Data & Tools', 'PostgreSQL', 85),
        ('Data & Tools', 'Supabase', 80),
        ('Data & Tools', 'Git / GitHub', 90),
        ('Data & Tools', 'Postman', 85)
    ]
    for idx, (cat, name, val) in enumerate(skills):
        Skill.objects.create(name=name, category=cat, ordering=val) # Using ordering to store progress value out of 100 for now

    print("Creating Education...")
    Education.objects.create(
        institution="JKUAT (Jomo Kenyatta University of Agriculture and Technology)",
        qualification="Bachelor's Degree",
        field="Business Information Technology (BBIT)",
        start_date="2021",
        end_date="Present"
    )

    print("Creating Experience...")
    Experience.objects.create(
        role="Freelance Full-Stack Developer",
        organization="Self-Employed",
        location="Kenya",
        start_date="2022",
        current=True,
        description="Developing custom web applications, mobile apps, and business management systems (including e-commerce and stock management solutions). Focused on delivering clean code, robust backend architectures using Django and PostgreSQL, and intuitive frontend experiences."
    )

    print("Creating Project Categories...")
    cat_mobile = ProjectCategory.objects.create(name="Mobile Applications", slug="mobile-applications")
    cat_web = ProjectCategory.objects.create(name="Web Applications", slug="web-applications")
    cat_backend = ProjectCategory.objects.create(name="Backend Systems", slug="backend-systems")

    print("Creating Technologies...")
    tech_django = Technology.objects.create(name="Django", slug="django")
    tech_drf = Technology.objects.create(name="Django REST Framework", slug="django-rest-framework")
    tech_python = Technology.objects.create(name="Python", slug="python")
    tech_postgres = Technology.objects.create(name="PostgreSQL", slug="postgresql")
    tech_supabase = Technology.objects.create(name="Supabase", slug="supabase")
    tech_flutter = Technology.objects.create(name="Flutter", slug="flutter")
    tech_dart = Technology.objects.create(name="Dart", slug="dart")
    tech_react = Technology.objects.create(name="React", slug="react")

    print("Creating Projects...")
    
    # Project 1: JoseKiarie Pharmacy
    p1 = Project.objects.create(
        title="JoseKiarie Pharmacy",
        slug="josekiarie-pharmacy",
        short_description="A comprehensive pharmacy stock and inventory management system.",
        description='''Architecture & Infrastructure
The system is built on a robust Django backend exposing RESTful APIs via Django REST Framework. The client is a cross-platform mobile application developed in Flutter. Data persistence is handled by PostgreSQL hosted on Supabase, ensuring scalability and secure remote connections.

Core Features & Implementation
- Role-Based Authentication: JWT token-based authentication separating Administrator and Pharmacist access, securing API endpoints.
- Inventory & Batch Management: Advanced stock tracking allowing products to be tracked by specific batches and expiry dates.
- Stock Movements: Comprehensive logging of all stock adjustments, purchases, and sales for perfect auditing.
- Supplier & Purchase Management: End-to-end tracking of suppliers, purchase orders, and automated stock increments upon order completion.
- Sales & Point of Sale (POS): A fast, reliable sales interface for processing customer transactions and generating instant receipts.
- Intelligent Dashboard & Reports: Real-time analytics showing low stock alerts, expiring batches, daily sales performance, and revenue reports.
- Automated Notifications: Background tasks triggering alerts for critical stock levels.

Current Status
The backend architecture, API endpoints (tested thoroughly via Postman), database schemas, and core Flutter UI are fully implemented. Next phases involve refining the analytical dashboard and deploying the mobile client.''',
        category=cat_backend,
        status="In Development",
        featured=True,
        ordering=1,
        year=2024,
        github_url="https://github.com/joseph001technology/JoseKiarie-Pharmacy"
    )
    p1.technologies.add(tech_django, tech_drf, tech_flutter, tech_dart, tech_postgres, tech_supabase)

    # Project 2: AgriFlow
    p2 = Project.objects.create(
        title="AgriFlow",
        slug="agriflow",
        short_description="Farm product ordering app connecting farmers to buyers.",
        description="AgriFlow is a farm-to-table e-commerce platform built to empower local farmers. It provides farmers with a dedicated dashboard to list fresh produce, manage inventory, and track orders. Buyers can browse, search by category, and place orders directly. Integrated with M-Pesa / Daraja APIs for seamless mobile payments, ensuring secure and fast transactions in the Kenyan market.",
        category=cat_mobile,
        status="Completed",
        featured=True,
        ordering=2,
        year=2024
    )
    p2.technologies.add(tech_django, tech_flutter, tech_python, tech_postgres)

    print("Data population completed successfully!")

if __name__ == '__main__':
    populate()
