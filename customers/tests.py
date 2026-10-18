from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class CustomerDashboardTests(TestCase):
    def test_customer_dashboard_uses_shared_dashboard_template(self):
        self.client.force_login(
            User.objects.create_user(username='dashboard_customer', password='secret123')
        )

        response = self.client.get(reverse('customers:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers/dashboard.html')
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response, 'Home Helper Finder')
        self.assertContains(response, 'Customer Dashboard')
        self.assertContains(response, reverse('pages:home'))
        self.assertContains(response, reverse('requests:list'))
