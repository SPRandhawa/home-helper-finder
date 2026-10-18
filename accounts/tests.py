from unittest.mock import patch

from django.contrib.auth.models import User
from django.db import IntegrityError
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
            verification_status=Helper.VERIFICATION_STATUS_PENDING,
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
            verification_status=Helper.VERIFICATION_STATUS_VERIFIED,
        )

        response = self.client.post(
            reverse('accounts:login', args=['helper']),
            {'username': 'helper_approved', 'password': 'secret123'},
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('helpers:list'))

    def test_verified_status_allows_login_even_if_approved_flag_is_false(self):
        User.objects.create_user(username='helper_verified', password='secret123')
        Helper.objects.create(
            name='Verified Helper',
            age=30,
            phone='1234567891',
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
            username='helper_verified',
            password='secret123',
            approved=False,
            verification_status=Helper.VERIFICATION_STATUS_VERIFIED,
        )

        response = self.client.post(
            reverse('accounts:login', args=['helper']),
            {'username': 'helper_verified', 'password': 'secret123'},
            follow=False,
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('helpers:list'))


class CustomerSignupTests(TestCase):
    def setUp(self):
        session = self.client.session
        session['signup_consent_customer'] = True
        session.save()

    def test_customer_signup_creates_django_user_and_logs_them_in(self):
        response = self.client.post(
            reverse('accounts:create_account', args=['customer']),
            {
                'username': 'new_customer',
                'password1': 'A-Long-Unique-Password-2026!',
                'password2': 'A-Long-Unique-Password-2026!',
            },
        )

        user = User.objects.get(username='new_customer')
        self.assertTrue(user.check_password('A-Long-Unique-Password-2026!'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('customers:dashboard'))
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)
        self.assertNotIn('signup_consent_customer', self.client.session)

    def test_customer_signup_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse('accounts:create_account', args=['customer']),
            {
                'username': 'new_customer',
                'password1': 'A-Long-Unique-Password-2026!',
                'password2': 'A-Different-Password-2026!',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/create_customer.html')
        self.assertFalse(User.objects.filter(username='new_customer').exists())


class HelperSignupTests(TestCase):
    def setUp(self):
        session = self.client.session
        session['signup_consent_helper'] = True
        session.save()

    def test_helper_signup_creates_login_and_profile_records(self):
        response = self.client.post(
            reverse('accounts:create_account', args=['helper']),
            {
                'username': 'new_helper',
                'password': 'helper-password-123',
                'name': 'New Helper',
                'age': '30',
                'phone': '1234567890',
                'gender': 'Female',
                'address': 'Main Street',
                'pincode': '560001',
                'marital_status': 'Single',
                'children': '0',
                'email': 'new-helper@example.com',
                'skills': 'cleaning',
                'work_time': '10 AM - 5 PM',
                'food_pref': 'Veg Only',
                'work_pref': 'Any Family',
                'status': 'Available',
            },
        )

        user = User.objects.get(username='new_helper')
        helper = Helper.objects.get(username='new_helper')
        self.assertTrue(user.check_password('helper-password-123'))
        self.assertEqual(helper.password, user.password)
        self.assertNotEqual(helper.password, 'helper-password-123')
        self.assertFalse(helper.approved)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'waiting.html')

    @patch('accounts.views.Helper.objects.create', side_effect=IntegrityError)
    def test_helper_signup_rolls_back_login_if_profile_creation_fails(self, create_helper):
        response = self.client.post(
            reverse('accounts:create_account', args=['helper']),
            {
                'username': 'rollback_helper',
                'password': 'helper-password-123',
                'name': 'New Helper',
                'age': '30',
                'phone': '1234567890',
                'gender': 'Female',
                'address': 'Main Street',
                'pincode': '560001',
                'marital_status': 'Single',
                'children': '0',
                'skills': 'cleaning',
                'work_time': '10 AM - 5 PM',
                'food_pref': 'Veg Only',
                'work_pref': 'Any Family',
                'status': 'Available',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/create_helper.html')
        self.assertFalse(User.objects.filter(username='rollback_helper').exists())
