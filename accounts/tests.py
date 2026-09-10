from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from helpers.models import Helper


class HelperApprovalLoginFlowTests(TestCase):
    def test_pending_helper_login_shows_waiting_page(self):
        User.objects.create_user(username='helper_pending', password='secret123')
        Helper.objects.create(
            name='Pending Helper',
            age=30,
            phone='1234567890',
            gender='Female',
            address='Main Street',
            pincode='560001',
            marital_status='Single',
            children=0,
            email='helper@example.com',
            skills='cleaning',
            work_time='10 AM - 5 PM',
            food_pref='Veg Only',
            work_pref='Full Time',
            status='Available',
            username='helper_pending',
            password='secret123',
            approved=False,
        )

        response = self.client.post(
            reverse('accounts:login', args=['helper']),
            {'username': 'helper_pending', 'password': 'secret123'},
            follow=False,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'waiting.html')

    def test_approved_helper_login_redirects_to_helper_dashboard(self):
        User.objects.create_user(username='helper_approved', password='secret123')
        Helper.objects.create(
            name='Approved Helper',
            age=30,
            phone='1234567890',
            gender='Female',
            address='Main Street',
            pincode='560001',
            marital_status='Single',
            children=0,
            email='helper@example.com',
            skills='cleaning',
            work_time='10 AM - 5 PM',
            food_pref='Veg Only',
            work_pref='Full Time',
            status='Available',
            username='helper_approved',
            password='secret123',
            approved=True,
        )

        response = self.client.post(
            reverse('accounts:login', args=['helper']),
            {'username': 'helper_approved', 'password': 'secret123'},
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('helpers:list'))
