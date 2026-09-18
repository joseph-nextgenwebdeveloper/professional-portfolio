from django.test import TestCase
from .models import ClientProjectRequest
from portfolio.models import Project, ProjectCategory


class RequestsTests(TestCase):
    def setUp(self):
        cat = ProjectCategory.objects.create(name="Management Systems")
        self.ref_project = Project.objects.create(
            title="Pharmacy System",
            tagline="Inventory control",
            category=cat,
            status="Completed"
        )

    def test_project_request_submission_with_optional_budget(self):
        # Clients must NEVER be forced to disclose a budget
        response = self.client.post('/request-project/', {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+254700000000',
            'organisation': 'Enterprise Kenya',
            'project_type': 'web_system',
            'project_title': 'Hospital Stock Portal',
            'details': 'Need a role-based medicine inventory and dispensing application.',
            'budget_range': '', # Optional!
            'deadline': 'Q3 2024',
            'contact_method': 'Email'
        })
        
        # It should redirect on success
        self.assertEqual(response.status_code, 302)
        
        # Check database persistence
        self.assertEqual(ClientProjectRequest.objects.count(), 1)
        req = ClientProjectRequest.objects.first()
        self.assertEqual(req.name, 'John Doe')
        self.assertEqual(req.organisation, 'Enterprise Kenya')
        self.assertEqual(req.budget_range, '')
        self.assertEqual(req.status, 'New')

    def test_project_request_with_reference_project(self):
        response = self.client.post(f'/request-project/{self.ref_project.slug}/', {
            'name': 'Alice Maina',
            'email': 'alice@chemist.co.ke',
            'details': 'We need a system identical to your pharmacy case study.',
            'requested_project': self.ref_project.id
        })
        self.assertEqual(response.status_code, 302)
        req = ClientProjectRequest.objects.latest('submitted_at')
        self.assertEqual(req.requested_project, self.ref_project)
