from django.test import TestCase
from .models import ContactMessage


class ContactTests(TestCase):
    def test_contact_submission_saved_to_db(self):
        response = self.client.post('/contact/', {
            'name': 'Sarah Mwangi',
            'email': 'sarah@example.com',
            'subject': 'Internal Logistics System',
            'message': 'We would like to discuss building a custom inventory management system.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.name, 'Sarah Mwangi')
        self.assertEqual(msg.subject, 'Internal Logistics System')
        self.assertFalse(msg.is_read)
        self.assertIsNotNone(msg.submitted_at)
