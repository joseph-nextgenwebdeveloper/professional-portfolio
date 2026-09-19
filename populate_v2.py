"""
Portfolio data population script — v2
Run with: .venv\Scripts\python.exe populate_v2.py
Clears and repopulates all portfolio data with rich, production-quality content.
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from portfolio.models import Project, ProjectCategory, Technology, Service, ProjectImage
from profiles.models import (
    Profile, Skill, Education, Experience, ExperienceBullet, SocialLink, Certification
)


def populate():
    print("=" * 60)
    print("  Portfolio Database Population — Joseph Kiarie")
    print("=" * 60)

    # CLEAR
    print("\n[1/9] Clearing old records...")
    Profile.objects.all().delete()
    SocialLink.objects.all().delete()
    Skill.objects.all().delete()
    Education.objects.all().delete()
    Experience.objects.all().delete()
    Certification.objects.all().delete()
    Service.objects.all().delete()
    ProjectImage.objects.all().delete()
    Project.objects.all().delete()
    ProjectCategory.objects.all().delete()
    Technology.objects.all().delete()
    print("      Done")

    # PROFILE
    print("\n[2/9] Creating Profile...")
    profile = Profile.objects.create(
        name="Joseph Ngigi Kiarie",
        headline="Full-Stack Developer & Systems Architect",
        short_bio=(
            "I build dependable Django web backends, Flutter mobile applications, and "
            "PostgreSQL/Supabase database architectures for real Kenyan organisations — "
            "replacing paper records and spreadsheet chaos with systems that actually work in the field."
        ),
        long_bio=(
            "I am a BBIT student at Jomo Kenyatta University of Agriculture and Technology (JKUAT) "
            "and a practicing full-stack software engineer based in Nairobi, Kenya.\n\n"
            "My academic training gives me a double lens: I understand business operations, supply "
            "chains, and accounting workflows just as deeply as database normalisation, query "
            "execution plans, and REST API design.\n\n"
            "In local Kenyan organisations, software failures rarely happen because the UI was not "
            "shiny enough. They happen because inventory math did not account for concurrent orders, "
            "staff roles were not properly restricted, or offline mobile sync silently corrupted data. "
            "I engineer systems from the database outward."
        ),
        photo="profile/jose.jpg",
        location="Nairobi, Kenya",
        email="josephkiarie@kiariejosephdevworks.net",
        availability_status="Available for new client projects & technical consulting",
        response_time_statement="I typically respond within 24 business hours.",
        github_url="https://github.com/joseph001technology",
        linkedin_url="https://linkedin.com/in/josephkiarie",
    )
    print(f"      Created: {profile}")

    # SOCIAL LINKS
    print("\n[3/9] Creating Social Links...")
    social_data = [
        ("github",   "GitHub — @joseph001technology",             "https://github.com/joseph001technology",         "github",   0),
        ("linkedin", "LinkedIn — Joseph Kiarie",                  "https://linkedin.com/in/josephkiarie",           "linkedin", 1),
        ("whatsapp", "WhatsApp — Direct Message",                 "https://wa.me/254700000000",                     "whatsapp", 2),
        ("email",    "josephkiarie@kiariejosephdevworks.net",     "mailto:josephkiarie@kiariejosephdevworks.net",   "mail",     3),
    ]
    for platform, label, url, icon, order in social_data:
        SocialLink.objects.create(platform=platform, label=label, url=url, icon=icon,
                                  display_order=order, is_public=True)
    print(f"      {len(social_data)} links created")

    # SKILLS
    print("\n[4/9] Creating Skills...")
    skills_data = [
        ("Python & Django",              "Backend & Systems",       "Core Stack",   0),
        ("Django REST Framework (DRF)",  "Backend & Systems",       "Core Stack",   1),
        ("JWT Authentication & RBAC",   "Backend & Systems",       "Production",   2),
        ("M-Pesa Daraja Integration",   "Backend & Systems",       "Production",   3),
        ("Flutter & Dart",               "Mobile Development",      "Core Stack",   4),
        ("Cross-Platform Android/iOS",   "Mobile Development",      "Production",   5),
        ("Offline Sync Logic",           "Mobile Development",      "Production",   6),
        ("Responsive UI (360px+)",       "Mobile Development",      "Operational",  7),
        ("PostgreSQL & RDBMS Design",    "Databases & Storage",     "Core Stack",   8),
        ("Supabase (Cloud DB & Auth)",  "Databases & Storage",     "Core Stack",   9),
        ("SQL Query Optimisation",       "Databases & Storage",     "Intermediate", 10),
        ("Git & GitHub",                 "Tools & DevOps",          "Daily Driver", 11),
        ("Postman API Testing",          "Tools & DevOps",          "Daily Driver", 12),
        ("Linux Server Deployment",      "Tools & DevOps",          "Operational",  13),
        ("Business Analysis & Scoping", "Soft Skills & Business",  "Strong",       14),
        ("Systems Thinking",             "Soft Skills & Business",  "Strong",       15),
        ("Technical Documentation",      "Soft Skills & Business",  "Practised",    16),
    ]
    for name, cat, prof, order in skills_data:
        Skill.objects.create(name=name, category=cat, proficiency=prof, display_order=order, active=True)
    print(f"      {len(skills_data)} skills created")

    # EDUCATION
    print("\n[5/9] Creating Education...")
    Education.objects.create(
        institution="Jomo Kenyatta University of Agriculture and Technology (JKUAT)",
        qualification="Bachelor of Business Information Technology (BBIT)",
        field="Business Information Technology",
        start_date="2021",
        end_date="Present",
        notes=(
            "Core coursework: Software Engineering, Database Management Systems, "
            "Distributed Systems, Business Communication, Financial Accounting, "
            "Operations Research, and Information Systems Management."
        ),
        display_order=0,
    )
    print("      Education created")

    # EXPERIENCE
    print("\n[6/9] Creating Experience & Bullets...")
    exp1 = Experience.objects.create(
        organisation="Self-Employed / Freelance",
        role="Full-Stack Developer",
        location="Nairobi, Kenya",
        start_date="Jan 2023",
        end_date=None,
        current=True,
        description=(
            "Designing, building, and deploying end-to-end software systems for Kenyan "
            "businesses. Specialising in inventory management portals, Flutter mobile "
            "applications, and REST API backends with M-Pesa payment integration."
        ),
        display_order=0,
    )
    bullets1 = [
        "Architected the JoseKiarie Pharmacy Management System: Django DRF backend with JWT RBAC, Flutter mobile POS client, and PostgreSQL database with batch/FIFO expiry tracking.",
        "Built AgriFlow, a farm-to-buyer marketplace with M-Pesa Daraja STK Push payment integration and a Flutter mobile app.",
        "Designed normalised PostgreSQL schemas with concurrent stock reservation logic using SELECT FOR UPDATE inside atomic transactions.",
        "Set up Postman collections documenting every API endpoint for client handover and developer onboarding.",
        "Deployed Django applications on Linux VPS with Nginx and Gunicorn.",
    ]
    for i, text in enumerate(bullets1):
        ExperienceBullet.objects.create(experience=exp1, text=text, display_order=i)

    exp2 = Experience.objects.create(
        organisation="JKUAT — Academic Projects",
        role="Software Engineering Student & Project Lead",
        location="Thika, Kenya",
        start_date="2021",
        end_date="Present",
        current=True,
        description=(
            "Applying degree coursework in software engineering and database design to "
            "hands-on capstone and independent projects."
        ),
        display_order=1,
    )
    bullets2 = [
        "Led design and implementation of a multi-role pharmacy management system as an independent project demonstrating full-stack competency.",
        "Applied database normalisation theory (3NF) and RDBMS design principles directly to production PostgreSQL schemas.",
        "Practised business process mapping and requirements gathering before writing any code.",
    ]
    for i, text in enumerate(bullets2):
        ExperienceBullet.objects.create(experience=exp2, text=text, display_order=i)
    print("      2 experience entries with bullets created")

    # CERTIFICATIONS
    print("\n[7/9] Creating Certifications...")
    certs = [
        ("Python for Everybody Specialisation",  "Coursera / University of Michigan", "2023"),
        ("REST APIs with Django REST Framework",  "Udemy",                             "2023"),
        ("Flutter & Dart — The Complete Guide",   "Udemy",                             "2024"),
        ("PostgreSQL for Beginners to Advanced",  "Udemy",                             "2024"),
        ("Git & GitHub Complete Masterclass",     "Udemy",                             "2023"),
    ]
    for i, (title, issuer, date) in enumerate(certs):
        Certification.objects.create(title=title, issuer=issuer, date=date, display_order=i)
    print(f"      {len(certs)} certifications created")

    # SERVICES
    print("\n[8/9] Creating Services...")
    services = [
        {
            "title": "Management Portal & Admin System Development",
            "tagline": "Replace spreadsheets with a structured, role-restricted web portal",
            "description": "I design and build custom Django management portals for businesses — inventory, staff roles, purchase orders, approvals, and reporting dashboards with proper RBAC.",
            "icon": "server",
            "deliverables": "Django backend with Admin panel\nRole-Based Access Control (RBAC)\nDatabase design & normalised schema\nCRUD operations for inventory or records\nReporting dashboard with analytics\nPostman API documentation",
            "display_order": 0,
        },
        {
            "title": "Flutter Mobile Application Development",
            "tagline": "Cross-platform Android and iOS apps for field staff",
            "description": "Flutter mobile apps designed for reliable operation on 3G networks and entry-level Android devices — POS terminals, ordering apps, or field data collection.",
            "icon": "mobile",
            "deliverables": "Flutter mobile app for Android (and iOS)\nJWT token authentication\nREST API integration\nOffline-tolerant data handling\nResponsive UI tested on 360px devices\nAPK build for distribution",
            "display_order": 1,
        },
        {
            "title": "REST API Backend Design & Integration",
            "tagline": "Clean, documented, secure APIs for mobile or third-party consumption",
            "description": "Django REST Framework APIs with consistent endpoint design, JWT authentication, per-role protection, and Postman documentation for easy handover.",
            "icon": "api",
            "deliverables": "Django REST Framework API\nJWT authentication with refresh tokens\nPer-role permission classes\nPostman collection\nError handling & consistent JSON structure\nRate limiting and security headers",
            "display_order": 2,
        },
        {
            "title": "M-Pesa Daraja Payment Integration",
            "tagline": "STK Push and C2B payment flows for Safaricom M-Pesa",
            "description": "M-Pesa Daraja STK Push and C2B callback integration into Django backends — transaction verification, payment status webhooks, and receipt logging.",
            "icon": "shield",
            "deliverables": "Safaricom Daraja STK Push integration\nC2B payment callback handling\nTransaction logging\nSandbox-to-production configuration\nError handling for failed transactions",
            "display_order": 3,
        },
        {
            "title": "Database Architecture & PostgreSQL Design",
            "tagline": "Normalised schemas designed for correctness and concurrency",
            "description": "PostgreSQL schemas from requirements upward — entities, relationships, constraints, indices, concurrent reservation logic, and audit tables.",
            "icon": "database",
            "deliverables": "ER diagram and schema design\nNormalised schema (3NF minimum)\nDjango ORM model implementation\nMigrations and seed data scripts\nIndex strategy for performance\nSupabase or self-hosted configuration",
            "display_order": 4,
        },
    ]
    for s in services:
        Service.objects.create(is_active=True, **s)
    print(f"      {len(services)} services created")

    # TECHNOLOGIES & PROJECTS
    print("\n[9/9] Creating Technologies & Projects...")

    techs = {}
    tech_list = [
        ("Django 5/6",                   "django",                "Backend",        0),
        ("Django REST Framework",        "django-rest-framework", "Backend",        1),
        ("Python",                       "python",                "Backend",        2),
        ("PostgreSQL",                   "postgresql",            "Database",       3),
        ("Supabase",                     "supabase",              "Database",       4),
        ("Flutter",                      "flutter",               "Mobile",         5),
        ("Dart",                         "dart",                  "Mobile",         6),
        ("JWT Authentication",           "jwt-auth",              "Architecture",   7),
        ("M-Pesa Daraja",                "mpesa-daraja",          "Integrations",   8),
        ("Role-Based Access Control",    "rbac",                  "Architecture",   9),
        ("Nginx",                        "nginx",                 "Cloud & DevOps", 10),
        ("Gunicorn",                     "gunicorn",              "Cloud & DevOps", 11),
        ("Git & GitHub",                 "git-github",            "Tools",          12),
        ("Postman",                      "postman",               "Tools",          13),
        ("Linux VPS",                    "linux-vps",             "Cloud & DevOps", 14),
        ("HTML5 & CSS3",                 "html-css",              "Frontend",       15),
        ("JavaScript",                   "javascript",            "Frontend",       16),
        ("Batch/FIFO Inventory Logic",   "batch-fifo",            "Architecture",   17),
    ]
    for name, slug, cat, order in tech_list:
        t = Technology.objects.create(name=name, slug=slug, category=cat, display_order=order, active=True)
        techs[slug] = t

    cat_pharmacy = ProjectCategory.objects.create(name="Pharmacy & Healthcare Systems", slug="pharmacy-healthcare")
    cat_agri     = ProjectCategory.objects.create(name="Agriculture & Marketplace",     slug="agriculture-marketplace")
    cat_portal   = ProjectCategory.objects.create(name="Management Portals",            slug="management-portals")

    p1 = Project.objects.create(
        title="JoseKiarie Pharmacy Management System",
        slug="josekiarie-pharmacy-management-system",
        tagline="Full-stack inventory, POS, and staff-management system for a Nairobi pharmacy — Django DRF backend with Flutter mobile client.",
        short_description="Pharmacy management portal with JWT RBAC, batch/FIFO stock tracking, POS, supplier management, and a Flutter mobile client.",
        problem_statement=(
            "The pharmacy was managing stock levels, supplier invoices, batch expiry dates, and daily sales "
            "entirely on paper and disconnected Excel workbooks. No audit trail for stock movements, "
            "no early warning for expiring batches, no real-time sales visibility for management. "
            "Staff had unrestricted access, creating accountability gaps and accidental overwrites."
        ),
        solution=(
            "Multi-component management system:\n\n"
            "Backend: Django DRF REST API handling inventory, batch tracking, sales, supplier orders, "
            "staff authentication, and reporting.\n\n"
            "Auth & Permissions: JWT with two role tiers — Administrator and Pharmacist. "
            "Admins manage staff and adjust stock; pharmacists process sales only.\n\n"
            "Inventory & Batch System: Products tracked at batch level with expiry dates. "
            "Sales deduct from earliest batch (FIFO) to reduce waste.\n\n"
            "Flutter POS Client: Product search, cart management, quantity input, receipt generation, "
            "authenticated against the Django backend.\n\n"
            "Dashboard: Low-stock alerts, batches expiring within 30 days, daily sales totals."
        ),
        my_role=(
            "Sole engineer. Requirements gathering, PostgreSQL schema, Django models, DRF serialisers, "
            "JWT authentication, Flutter app architecture, API integration, Postman documentation, Linux VPS deployment."
        ),
        architecture_notes=(
            "Stack: Django 5, DRF, PostgreSQL via Supabase, Flutter, Nginx + Gunicorn.\n"
            "Key tables: Product, Batch, StockMovement, Sale, SaleItem, Supplier, PurchaseOrder, CustomUser.\n"
            "FIFO batch deduction: queryset ordered expiry_date ASC iterated inside atomic transaction with SELECT FOR UPDATE.\n"
            "Auth: SimpleJWT — 15-min access tokens, 7-day refresh tokens. Custom IsAdministrator / IsPharmacist permission classes."
        ),
        challenges=(
            "Concurrent stock deduction: Solved with database-level row locking (SELECT FOR UPDATE) in atomic transactions.\n"
            "Batch FIFO accuracy: Daily background task marks batches where expiry_date < today as exhausted.\n"
            "Flutter JWT refresh: Transparent token refresh via Dio interceptor with retry logic on 401 responses."
        ),
        outcomes=(
            "Backend fully operational with all API endpoints tested and documented via Postman. "
            "Flutter POS client functional on Android. Core inventory, batch tracking, and sales recording "
            "working in staging. Pending final client review before production deployment."
        ),
        category=cat_pharmacy,
        status="In Progress",
        year="2024",
        featured_image="projects/Agriflow-login.jpeg",
        is_featured=True,
        is_published=True,
        display_order=1,
        repo_url="https://github.com/joseph001technology/JoseKiarie-Pharmacy",
    )
    p1.technologies.add(
        techs["django"], techs["django-rest-framework"], techs["python"],
        techs["postgresql"], techs["supabase"], techs["flutter"], techs["dart"],
        techs["jwt-auth"], techs["rbac"], techs["batch-fifo"], techs["postman"],
        techs["nginx"], techs["gunicorn"],
    )

    p2 = Project.objects.create(
        title="AgriFlow — Farm-to-Buyer Marketplace",
        slug="agriflow-farm-to-buyer-marketplace",
        tagline="Flutter mobile marketplace connecting Kenyan smallholder farmers to local buyers with M-Pesa STK Push payment integration.",
        short_description="Mobile-first agri-commerce platform with farmer dashboards, product listing, order management, and M-Pesa Daraja integration.",
        problem_statement=(
            "Smallholder farmers sell produce at below-market prices because they have no direct channel to buyers "
            "beyond their immediate locality. No accessible, mobile-first platform let a farmer list produce "
            "and receive direct M-Pesa payment from a buyer."
        ),
        solution=(
            "Two-sided marketplace with separate dashboards for Farmers and Buyers.\n\n"
            "Farmer: Register farm, list produce with category, quantity, price, and photo. View and manage orders.\n\n"
            "Buyer: Browse by category, search by location, add to cart, checkout via M-Pesa STK Push.\n\n"
            "Backend: Django DRF handling user registration, product CRUD, order lifecycle, and M-Pesa Daraja callbacks."
        ),
        my_role=(
            "Sole engineer. Requirements, PostgreSQL schema, Django DRF API, M-Pesa Daraja integration, "
            "Flutter app architecture, farmer and buyer UI screens, API integration layer."
        ),
        architecture_notes=(
            "Stack: Django DRF, PostgreSQL, Flutter.\n"
            "Key models: Farm, Product, ProductCategory, Order, OrderItem, MpesaTransaction, CustomUser (user_type: farmer/buyer).\n"
            "M-Pesa flow: POST /api/payments/initiate/ → Daraja STK Push → Safaricom callback → update Order.status = paid."
        ),
        challenges=(
            "M-Pesa callback: Required publicly accessible endpoint; used ngrok for local testing.\n"
            "Two-role Flutter navigation: Conditional routing based on JWT payload user_type field."
        ),
        outcomes=(
            "Complete MVP: product listing, order flow, and M-Pesa STK Push in Safaricom sandbox. "
            "Flutter app running on Android. Pending production Daraja credentials."
        ),
        category=cat_agri,
        status="Completed",
        year="2024",
        featured_image="projects/Agriflow-home.jpeg",
        is_featured=True,
        is_published=True,
        display_order=2,
    )
    p2.technologies.add(
        techs["django"], techs["django-rest-framework"], techs["python"],
        techs["flutter"], techs["dart"], techs["postgresql"], techs["mpesa-daraja"], techs["jwt-auth"],
    )

    p3 = Project.objects.create(
        title="This Portfolio — Database-Driven Django Site",
        slug="joseph-kiarie-portfolio-site",
        tagline="Fully database-driven portfolio built with Django, server-rendered templates, and PostgreSQL — every section editable from Django Admin.",
        short_description="Professional portfolio built with Django, fully editable from Admin, no SPA framework.",
        problem_statement="Generic portfolio builders produce identical-looking sites and demonstrate no real engineering ability.",
        solution=(
            "Server-rendered Django site where every content block — profile, projects, services, experience, skills, "
            "social links — is stored relationally and editable from the Django Admin panel without touching code."
        ),
        my_role="Sole engineer. Full design system, backend architecture, template development, and data population.",
        architecture_notes=(
            "Framework: Django 6, server-rendered templates. CSS: Vanilla with custom properties, editorial light-first design.\n"
            "Typography: Fraunces + Inter + JetBrains Mono."
        ),
        category=cat_portal,
        status="In Progress",
        year="2025",
        featured_image="profile/about-pic.jpg",
        is_featured=False,
        is_published=True,
        display_order=3,
        live_url="https://kiariejosephdevworks.net",
    )
    p3.technologies.add(
        techs["django"], techs["python"], techs["postgresql"], techs["html-css"], techs["javascript"],
    )

    ProjectImage.objects.create(
        project=p2,
        image="projects/Agriflow-login.jpeg",
        caption="AgriFlow Mobile Marketplace — Login & STK Push Authentication Screen",
        display_order=1
    )
    ProjectImage.objects.create(
        project=p1,
        image="projects/Agriflow-home.jpeg",
        caption="JoseKiarie Pharmacy — Inventory & Batch FIFO Dashboard Interface",
        display_order=1
    )

    print(f"      3 projects, {len(tech_list)} technologies, 3 categories, {ProjectImage.objects.count()} project images created")

    print("\n" + "=" * 60)
    print("  Population complete!")
    print("=" * 60)
    from portfolio.models import Project as P
    from profiles.models import Profile as Pr
    print(f"  Profile:         {Pr.objects.count()}")
    print(f"  Social Links:    {SocialLink.objects.count()}")
    print(f"  Skills:          {Skill.objects.count()}")
    print(f"  Education:       {Education.objects.count()}")
    print(f"  Experience:      {Experience.objects.count()} (with {ExperienceBullet.objects.count()} bullets)")
    print(f"  Certifications:  {Certification.objects.count()}")
    print(f"  Services:        {Service.objects.count()}")
    print(f"  Technologies:    {Technology.objects.count()}")
    print(f"  Projects:        {P.objects.count()} (featured: {P.objects.filter(is_featured=True).count()})")
    print(f"  Categories:      {ProjectCategory.objects.count()}")
    print()


if __name__ == "__main__":
    populate()
