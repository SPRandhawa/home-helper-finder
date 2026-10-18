from django.contrib import admin
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse

from helpers.admin import HelperAdmin
from helpers.models import Helper


class HelperPincodeModelTest(TestCase):
    def test_helper_model_can_store_pincode(self):
        helper = Helper.objects.create(
            name='Test Helper',
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
            username='testhelper',
            password='secret',
            approved=False,
        )

        self.assertEqual(helper.pincode, '560001')


class HelperDashboardTests(TestCase):
    def test_dashboard_displays_saved_helper_profile(self):
        user = User.objects.create_user(username='dashboard_helper', password='secret123')
        Helper.objects.create(
            name='Dashboard Helper',
            age=30,
            phone='1234567890',
            gender='Female',
            address='Main Street',
            pincode='560001',
            marital_status='Single',
            children=0,
            email='dashboard-helper@example.com',
            skills='cleaning',
            work_time='10 AM - 5 PM',
            food_pref='Veg Only',
            work_pref='Any Family',
            status='Available',
            username='dashboard_helper',
            password=user.password,
            approved=False,
        )
        self.client.force_login(user)

        response = self.client.get(reverse('helpers:list'))

        self.assertEqual(response.status_code, 200)
        self.assertIn(('Name', 'Dashboard Helper'), response.context['account_details'])
        self.assertIn(('Pincode', '560001'), response.context['account_details'])
        self.assertContains(response, 'Dashboard Helper')


class HelperApprovalAdminTests(TestCase):
    def setUp(self):
        self.helper = Helper.objects.create(
            name='Approval Helper',
            age=30,
            phone='1234567890',
            gender='Female',
            address='Main Street',
            pincode='560001',
            marital_status='Single',
            children=0,
            skills='cleaning',
            work_time='10 AM - 5 PM',
            food_pref='Veg Only',
            work_pref='Any Family',
            username='approval_helper',
            password='secret',
        )
        self.admin_request = RequestFactory().post('/admin/helpers/helper/')
        self.admin_request.user = User.objects.create_superuser(
            username='site_admin',
            email='admin@example.com',
            password='site-admin-password-123',
        )
        self.helper_admin = HelperAdmin(Helper, admin.site)

    def test_mark_verified_also_sets_approved(self):
        self.helper_admin.mark_verified(
            self.admin_request,
            Helper.objects.filter(pk=self.helper.pk),
        )

        self.helper.refresh_from_db()
        self.assertEqual(
            self.helper.verification_status,
            Helper.VERIFICATION_STATUS_VERIFIED,
        )
        self.assertTrue(self.helper.approved)

    def test_mark_rejected_clears_approved(self):
        Helper.objects.filter(pk=self.helper.pk).update(approved=True)

        self.helper_admin.mark_rejected(
            self.admin_request,
            Helper.objects.filter(pk=self.helper.pk),
        )

        self.helper.refresh_from_db()
        self.assertEqual(
            self.helper.verification_status,
            Helper.VERIFICATION_STATUS_REJECTED,
        )
        self.assertFalse(self.helper.approved)

    def test_saving_verified_status_also_sets_approved(self):
        self.helper.verification_status = Helper.VERIFICATION_STATUS_VERIFIED

        self.helper_admin.save_model(
            self.admin_request,
            self.helper,
            form=None,
            change=True,
        )

        self.helper.refresh_from_db()
        self.assertTrue(self.helper.approved)
