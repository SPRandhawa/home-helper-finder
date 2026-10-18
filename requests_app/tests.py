from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class DashboardPageTests(TestCase):
    def test_request_pages_render_the_shared_dashboard(self):
        for route_name in ('requests:list', 'requests:create'):
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'app_dashboard.html')
                self.assertContains(response, 'Home Helper Finder')

    def test_chatbot_home_renders_the_shared_dashboard(self):
        response = self.client.get(reverse('chatbot:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_dashboard.html')
        self.assertContains(response, 'Home Helper assistant')

    def test_account_dashboard_renders_the_shared_dashboard(self):
        user = User.objects.create_user(username='dashboard_user', password='secret123')
        self.client.force_login(user)

        response = self.client.get(reverse('accounts:dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_dashboard.html')
        self.assertContains(response, 'Welcome to your account')

    def test_dashboard_logout_logs_user_out_and_returns_home(self):
        user = User.objects.create_user(username='logout_user', password='secret123')
        self.client.force_login(user)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('pages:home'))
        self.assertNotIn('_auth_user_id', self.client.session)
