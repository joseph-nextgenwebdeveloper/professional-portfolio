# Joseph Kiarie — Developer Portfolio & Project Request System

A production-ready, database-driven Django personal portfolio and client project intake system for **Joseph Kiarie** (Full-Stack Developer & Systems Architect, BBIT student at JKUAT, Nairobi).

Designed with an editorial, light-first aesthetic (deep navy/ink, warm cream, forest green, and terracotta amber) with high contrast, zero artificial AI gradients/glows, and full responsiveness down to 360px mobile screens.

---

## Architecture & Production Setup

* **Server-Rendered Architecture:** Clean Django templates with Semantic HTML5 and Vanilla CSS. No SPA, no heavy build tools, minimal JavaScript, and zero external CSS CDNs.
* **Production Database (Supabase PostgreSQL):** Configured via the `DATABASE_URL` environment variable using `dj_database_url`. SQLite is used strictly for local development fallback.
* **Pluggable Media Storage (`django-storages`):** Configured via Django's standard `STORAGES` dictionary. Supports Supabase Storage / S3 / GCS via `DEFAULT_FILE_STORAGE` environment variable in production, falling back to local filesystem storage during `DEBUG=True`.
* **Database-First Submissions:** Both Project Requests and Contact Messages are committed to PostgreSQL *first* before attempting email notifications. If email dispatch fails, submissions are never lost.
* **Admin-Editable Models:** Profile (singleton), Projects (with case-study fields, published flags), ProjectImages, Technologies, Services, Experience (with bullet inlines), Education, Certifications, and Inquiries.

---

## Quick Start & Execution Order

Follow these steps to run the application locally:

### 1. Activate Virtual Environment & Install Dependencies
```bash
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` (or configure your `.env` directly):
```env
SECRET_KEY=your-secure-production-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
PORTFOLIO_NOTIFICATION_EMAIL=your-email@gmail.com
```

### 3. Run Database Migrations
```bash
python manage.py migrate
```

### 4. Seed Real Project & Profile Data
Populates the database with real case studies (**JoseKiarie Pharmacy** and **AgriFlow**), services, technologies, education, and profile:
```bash
python manage.py seed_portfolio_data
```

### 5. Create Superuser (For Django Admin)
```bash
python manage.py createsuperuser
```

### 6. Run Automated Tests
```bash
python manage.py test
```

### 7. Start Development Server
```bash
python manage.py runserver
```

Visit the application at: `http://127.0.0.1:8000/`  
Access Django Admin at: `http://127.0.0.1:8000/admin/`

---

## Environment Variables Reference

| Variable | Required in Prod | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | Yes | Unique, secret cryptographic key for Django sessions & CSRF. |
| `DEBUG` | Yes (set `False`) | Toggles debug mode (`False` in production). |
| `ALLOWED_HOSTS` | Yes | Comma-separated list of production domain names. |
| `DATABASE_URL` | Yes | Connection string to Supabase PostgreSQL or cloud DB. |
| `DEFAULT_FILE_STORAGE` | Optional | Custom storage backend class (e.g. `storages.backends.s3boto3.S3Boto3Storage`). |
| `EMAIL_BACKEND` | Optional | Defaults to console in `DEBUG`, SMTP in production. |
| `EMAIL_HOST` | Prod SMTP | SMTP host (e.g. `smtp.gmail.com` or SendGrid/Postmark). |
| `EMAIL_PORT` | Prod SMTP | Port for SMTP (e.g. `587`). |
| `EMAIL_HOST_USER` | Prod SMTP | Authentication username/email for SMTP. |
| `EMAIL_HOST_PASSWORD` | Prod SMTP | App-specific password or API token for SMTP. |
| `PORTFOLIO_NOTIFICATION_EMAIL` | Optional | Email address that receives project inquiries and messages. |

---

## Project Case Studies Included

1. **JoseKiarie Pharmacy — Stock & Inventory Management System:**
   * Staff-facing inventory and dispensing control system.
   * Architecture: Django REST Framework, Flutter client, Supabase PostgreSQL.
   * Features: Role-based permissions, batch-level FIFO expiration tracking, and atomic inventory decrementing.
2. **AgriFlow — Agricultural Supply & Farm-to-Consumer Platform:**
   * Mobile application connecting smallholder Kenyan farmers directly to consumers to reduce post-harvest loss.
   * Architecture: Flutter + Django REST Framework, PostgreSQL.
   * Integrations: Safaricom Daraja M-Pesa STK Push sandbox and cash-on-delivery flows.
