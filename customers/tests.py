from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class CustomerDashboardTests(TestCase):
    def test_dashboard_displays_saved_customer_login(self):
        user = User.objects.create_user(username='dashboard_customer', password='secret123')
        self.client.force_login(user)

        response = self.client.get(reverse('customers:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertIn(('Username', 'dashboard_customer'), response.context['account_details'])
        self.assertContains(response, 'dashboard_customer')
