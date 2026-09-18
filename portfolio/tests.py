from django.test import TestCase
from portfolio.models import Project, ProjectCategory, Technology, Service


class PortfolioTests(TestCase):
    def setUp(self):
        self.category = ProjectCategory.objects.create(name="Web App")
        self.project = Project.objects.create(
            title="Test Project",
            tagline="A test project",
            problem_statement="Operational bottleneck",
            solution="Django and PostgreSQL system",
            category=self.category,
            status="Completed",
            is_published=True,
            is_featured=True
        )
        self.draft_project = Project.objects.create(
            title="Internal Secret Project",
            tagline="Draft system",
            category=self.category,
            status="In Progress",
            is_published=False
        )

    def test_project_creation(self):
        self.assertEqual(self.project.title, "Test Project")
        self.assertEqual(self.project.slug, "test-project")
        self.assertEqual(self.project.category.name, "Web App")

    def test_project_list_view_filters_unpublished(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Project")
        # Unpublished project must never be shown on public index
        self.assertNotContains(response, "Internal Secret Project")

    def test_project_detail_view_public(self):
        response = self.client.get(f'/projects/{self.project.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Project")
        self.assertContains(response, "Operational bottleneck")

    def test_unpublished_project_returns_404(self):
        response = self.client.get(f'/projects/{self.draft_project.slug}/')
        self.assertEqual(response.status_code, 404)
