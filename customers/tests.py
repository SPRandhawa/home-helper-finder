from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse


class CustomerLoginRouteTests(TestCase):
    def test_legacy_customer_login_route_uses_shared_login_form(self):
        response = self.client.get(reverse('customers:login_customers'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertEqual(response.context['destination'], 'customer')
