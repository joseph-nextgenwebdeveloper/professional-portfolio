from django.core.management.base import BaseCommand
from portfolio.models import Project, ProjectCategory, Technology, Service
from profiles.models import (
    Profile,
    SocialLink,
    Experience,
    ExperienceBullet,
    Education
)


class Command(BaseCommand):
    help = 'Seeds database with real projects (JoseKiarie Pharmacy, AgriFlow), services, technologies, and profile metadata'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding portfolio data..."))

        # 1. Profile
        profile, created = Profile.objects.get_or_create(
            id=1,
            defaults={
                'name': 'Joseph Kiarie',
                'headline': 'Full-Stack Developer & Systems Architect',
                'short_bio': 'BBIT student at JKUAT engineering dependable web platforms, cross-platform mobile systems, and database architectures for businesses and operating organizations in Kenya.',
                'long_bio': 'I design and build software systems that replace fragile manual spreadsheets and disconnected records with unified, role-based digital tools. My primary technical foundation spans Python/Django on the backend, Flutter on mobile, and PostgreSQL/Supabase for structured, reliable data management. I build for real enterprise utility, predictable performance on mobile data, and practical day-to-day operations.',
                'location': 'Nairobi, Kenya',
                'availability_status': 'Available for client projects & technical consulting',
                'response_time_statement': 'I typically respond within 24 hours to project inquiries.',
                'email': 'TODO: Add public email in Admin',
                'phone': 'TODO: Add phone/WhatsApp in Admin',
                'github_url': 'https://github.com/joseph001technology',
                'linkedin_url': '',
            }
        )
        if not created:
            profile.name = 'Joseph Kiarie'
            profile.headline = 'Full-Stack Developer & Systems Architect'
            profile.location = 'Nairobi, Kenya'
            profile.save()
        self.stdout.write(self.style.SUCCESS(f"Profile: {profile.name}"))

        # 2. Social Links
        SocialLink.objects.all().delete()
        socials = [
            {'platform': 'github', 'label': 'GitHub', 'url': 'https://github.com/joseph001technology', 'icon': 'github', 'display_order': 1},
            {'platform': 'linkedin', 'label': 'LinkedIn', 'url': 'https://linkedin.com/in/TODO-add-linkedin-in-admin', 'icon': 'linkedin', 'display_order': 2},
            {'platform': 'whatsapp', 'label': 'WhatsApp', 'url': 'https://wa.me/TODO-add-number-in-admin', 'icon': 'whatsapp', 'display_order': 3},
            {'platform': 'email', 'label': 'Direct Email', 'url': 'mailto:TODO-add-email-in-admin', 'icon': 'mail', 'display_order': 4},
        ]
        for s in socials:
            SocialLink.objects.create(**s)
        self.stdout.write(self.style.SUCCESS("Seeded Social Links."))

        # 3. Technologies
        tech_data = [
            ('Django', 'Backend', 'django', 1),
            ('Django REST Framework', 'Backend', 'api', 2),
            ('Flutter', 'Mobile', 'flutter', 3),
            ('PostgreSQL', 'Database', 'database', 4),
            ('Supabase', 'Database', 'supabase', 5),
            ('Python', 'Language', 'python', 6),
            ('Dart', 'Language', 'dart', 7),
            ('M-Pesa Daraja API', 'Integrations', 'mpesa', 8),
            ('Docker / Linux', 'DevOps', 'server', 9),
            ('Git / GitHub', 'Tools', 'git', 10),
            ('Postman', 'Tools', 'postman', 11),
        ]
        tech_map = {}
        for name, cat, icon, order in tech_data:
            t, _ = Technology.objects.get_or_create(
                name=name,
                defaults={'category': cat, 'icon_name': icon, 'display_order': order, 'active': True}
            )
            tech_map[name] = t
        self.stdout.write(self.style.SUCCESS("Seeded Technologies."))

        # 4. Categories
        cat_sys, _ = ProjectCategory.objects.get_or_create(
            name='Enterprise Management Systems',
            defaults={'description': 'Staff-facing operations, inventory, and administrative platforms.'}
        )
        cat_mobile, _ = ProjectCategory.objects.get_or_create(
            name='Mobile & Consumer Applications',
            defaults={'description': 'Cross-platform mobile applications with real-time transactional sync.'}
        )

        # 5. Projects (Real data only, no invented metrics or fake URLs)
        # Project 1: JoseKiarie Pharmacy
        pharmacy, p_created = Project.objects.update_or_create(
            slug='josekiarie-pharmacy',
            defaults={
                'title': 'JoseKiarie Pharmacy — Stock & Inventory Management System',
                'tagline': 'Staff-facing pharmacy inventory and dispensing management system built with a Django backend, Flutter client, and Supabase PostgreSQL.',
                'problem_statement': (
                    'Community and hospital-affiliated pharmacies frequently struggle with inventory shrinkage, '
                    'stockouts of life-saving medicines, untracked batch expiration dates, and lack of accountability '
                    'across cashier and dispensing shifts when relying on paper ledgers or generic point-of-sale systems.'
                ),
                'solution': (
                    'Architected a role-based, internal staff management platform. The system cleanly separates '
                    'pharmacist dispensing workflows from cashier reconciliation and inventory auditing, '
                    'maintaining strict audit trails across batch expiration dates, unit dosage tracking, supplier '
                    'purchase orders, and daily shift balancing.'
                ),
                'my_role': (
                    'Full-Stack Engineer & Systems Architect. Responsible for relational database schema modeling '
                    'in PostgreSQL/Supabase, designing authenticated REST endpoints with Django, and implementing '
                    'the responsive staff-facing client application in Flutter.'
                ),
                'architecture_notes': (
                    'Django REST Framework backend configured with Supabase PostgreSQL. JWT-based role authentication '
                    'for Staff, Pharmacist, and Admin tiers. Relational tables enforce atomic inventory decrementing '
                    'upon dispensation, batch tracking with automated expiry window alerts, and immutable sales log generation.'
                ),
                'challenges': (
                    'Ensuring atomic stock transactions during peak customer dispensing hours without race conditions; '
                    'implementing batch-level FIFO (First-In, First-Out) expiration alerts so older medicine batches '
                    'are prioritized before expiry.'
                ),
                'outcomes': '',  # Left blank intentionally as instructed
                'category': cat_sys,
                'status': 'Completed',
                'year': '2024',
                'live_url': '',  # Left blank intentionally
                'repo_url': '',  # Left blank intentionally
                'is_featured': True,
                'is_published': True,
                'display_order': 1,
            }
        )
        pharmacy.technologies.set([
            tech_map['Django'],
            tech_map['Django REST Framework'],
            tech_map['Flutter'],
            tech_map['PostgreSQL'],
            tech_map['Supabase'],
            tech_map['Python'],
        ])

        # Project 2: AgriFlow
        agriflow, a_created = Project.objects.update_or_create(
            slug='agriflow',
            defaults={
                'title': 'AgriFlow — Agricultural Supply & Direct Farm-to-Consumer Platform',
                'tagline': 'Farm-product ordering application connecting Kenyan farmers directly to consumers, featuring Daraja M-Pesa sandbox integration and payment-on-delivery flows.',
                'problem_statement': (
                    'Smallholder Kenyan farmers suffer significant post-harvest loss due to fragmented middleman '
                    'distribution networks, opaque pricing structures, and delays in connecting perishable fresh '
                    'produce directly to urban households and retail buyers.'
                ),
                'solution': (
                    'Engineered a direct agricultural marketplace connecting local growers directly to retail buyers and consumers. '
                    'Incorporates produce listing management, order dispatch tracking, delivery verification, and '
                    'flexible payment workflows including Daraja M-Pesa mobile money sandbox and cash-on-delivery reconciliation.'
                ),
                'my_role': (
                    'Full-Stack Mobile & Backend Developer. Designed the DRF REST API endpoints, integrated Daraja M-Pesa '
                    'STK Push sandbox webhooks, implemented JWT authentication, and structured the Flutter mobile ordering interface.'
                ),
                'architecture_notes': (
                    'Django REST Framework backend backed by PostgreSQL. Mobile client built in Flutter with Provider state '
                    'management. Safaricom Daraja M-Pesa API sandbox integration with webhook callback endpoints to handle '
                    'asynchronous payment confirmation and transaction status reconciliation.'
                ),
                'challenges': (
                    'Handling asynchronous M-Pesa callback states reliably over intermittent mobile network connectivity; '
                    'architecting clean failover states for payment-on-delivery vs digital mobile money.'
                ),
                'outcomes': '',  # Left blank intentionally as instructed
                'category': cat_mobile,
                'status': 'Completed',
                'year': '2024',
                'live_url': '',  # Left blank intentionally
                'repo_url': '',  # Left blank intentionally
                'is_featured': True,
                'is_published': True,
                'display_order': 2,
            }
        )
        agriflow.technologies.set([
            tech_map['Flutter'],
            tech_map['Django REST Framework'],
            tech_map['PostgreSQL'],
            tech_map['M-Pesa Daraja API'],
            tech_map['Python'],
            tech_map['Dart'],
        ])
        self.stdout.write(self.style.SUCCESS("Seeded real projects: JoseKiarie Pharmacy & AgriFlow."))

        # 6. Services (What I Build)
        Service.objects.all().delete()
        services_data = [
            {
                'title': 'Internal Management Systems & Operational Portals',
                'tagline': 'Custom staff-facing web applications that replace error-prone spreadsheets.',
                'description': 'End-to-end operational software built on Django and PostgreSQL. Designed specifically for internal staff workflows, inventory tracking, role-based authorizations, and granular audit trails.',
                'deliverables': 'Role-based access control (RBAC)\nAtomic inventory & stock management\nAdmin dashboard & reporting\nAudit logging & automated data backups',
                'icon': 'server',
                'display_order': 1,
            },
            {
                'title': 'Cross-Platform Mobile Applications',
                'tagline': 'High-performance Flutter apps for Android and iOS.',
                'description': 'Mobile client applications crafted with Flutter and Dart. Engineered for smooth performance on entry-level Android devices and designed to function predictably on variable Kenyan mobile data connections.',
                'deliverables': 'Offline-first caching\nClean state management\nResponsive interfaces down to 360px\nREST API synchronization',
                'icon': 'mobile',
                'display_order': 2,
            },
            {
                'title': 'RESTful API Engineering & Payment Gateways',
                'tagline': 'Robust backend microservices and mobile money integrations.',
                'description': 'Clean, documented REST APIs using Django REST Framework. Specialised in asynchronous webhook handling, JWT authentication, and Safaricom Daraja M-Pesa STK Push / C2B integration.',
                'deliverables': 'Safaricom Daraja M-Pesa STK Push integration\nJWT & token-based authentication\nPostman test collections & documentation\nWebhook idempotency & retry logic',
                'icon': 'api',
                'display_order': 3,
            },
            {
                'title': 'Relational Database Architecture & Supabase',
                'tagline': 'Structured, normalized schemas optimized for integrity and scale.',
                'description': 'Relational data modeling with PostgreSQL and Supabase. Implementing rigorous foreign keys, constraints, composite indexes, and migration strategies so data never corrupts under concurrent usage.',
                'deliverables': 'PostgreSQL schema modeling & migrations\nSupabase cloud setup & security rules\nQuery optimization & indexing\nAutomated backup procedures',
                'icon': 'database',
                'display_order': 4,
            },
        ]
        for s in services_data:
            Service.objects.create(**s)
        self.stdout.write(self.style.SUCCESS("Seeded Services."))

        # 7. (Skills were merged into Technologies - nothing to seed here.)

        # 8. Experience
        Experience.objects.all().delete()
        exp = Experience.objects.create(
            organisation='Mfano Bora Africa Limited',
            role='Software Engineering Attache / Intern',
            location='Nairobi, Kenya',
            start_date='TODO: Set start date in Admin',
            end_date='TODO: Set end date in Admin',
            current=False,
            description='Technical attachment contributing to software systems, internal workflows, and practical engineering operations.',
            display_order=1
        )
        ExperienceBullet.objects.create(
            experience=exp,
            text='Assisted in software development workflows, database administration, and operational systems support.',
            display_order=1
        )
        ExperienceBullet.objects.create(
            experience=exp,
            text='Collaborated with technical team members to diagnose system issues, write clean code, and document application behavior.',
            display_order=2
        )
        self.stdout.write(self.style.SUCCESS("Seeded Experience."))

        # 9. Education
        Education.objects.all().delete()
        Education.objects.create(
            institution='Jomo Kenyatta University of Agriculture and Technology (JKUAT)',
            qualification='Bachelor of Business Information Technology (BBIT)',
            field='Business Information Technology & Software Engineering',
            start_date='2022',
            end_date='Present (Ongoing)',
            notes='Coursework encompasses Enterprise Systems Architecture, Database Design & Management (RDBMS), Object-Oriented Programming, Data Communications & Networks, and IT Project Management.',
            display_order=1
        )
        self.stdout.write(self.style.SUCCESS("Seeded Education."))

        self.stdout.write(self.style.SUCCESS("\n==> Portfolio database seeded successfully!"))
