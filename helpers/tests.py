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
    def test_verified_helper_sees_empty_dashboard(self):
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
            approved=True,
            verification_status=Helper.VERIFICATION_STATUS_VERIFIED,
        )
        self.client.force_login(user)

        response = self.client.get(reverse('helpers:list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'helpers/dashboard.html')
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response, 'Home Helper Finder')
        self.assertContains(response, 'Maid Dashboard')
        self.assertContains(response, reverse('pages:home'))
        self.assertContains(response, reverse('pages:help'))
        self.assertNotContains(response, 'Dashboard Helper')

    def test_helper_profile_shows_signup_information_only(self):
        user = User.objects.create_user(username='profile_helper', password='secret123')
        Helper.objects.create(
            name='Profile Helper',
            age=30,
            phone='1234567893',
            gender='Female',
            address='Main Street',
            pincode='560001',
            marital_status='Single',
            children=0,
            email='profile-helper@example.com',
            skills='cleaning',
            work_time='10 AM - 5 PM',
            working_days=['Monday', 'Wednesday'],
            food_pref='Veg Only',
            work_pref='Any Family',
            status='Available',
            username='profile_helper',
            password='stored-secret',
            verification_status=Helper.VERIFICATION_STATUS_VERIFIED,
        )
        self.client.force_login(user)

        response = self.client.get(reverse('helpers:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'helpers/profile.html')
        for signup_value in (
            'Profile Helper',
            '1234567893',
            'profile-helper@example.com',
            'Main Street',
            'Monday',
            'Wednesday',
            'Veg Only',
        ):
            self.assertContains(response, signup_value)
        self.assertNotContains(response, 'stored-secret')
        self.assertNotContains(response, 'verification_status')
        self.assertNotContains(response, 'Signup uploads')
        self.assertNotContains(response, 'Aadhaar front')

    def test_helper_can_update_profile_fields_and_photo(self):
        from io import BytesIO
        import tempfile

        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile

        user = User.objects.create_user(username='editable_helper', password='secret123')
        helper = Helper.objects.create(
            name='Editable Helper',
            age=30,
            phone='1234567894',
            gender='Female',
            address='Main Street',
            pincode='560001',
            marital_status='Single',
            children=0,
            skills='cleaning',
            work_time='10 AM - 5 PM',
            working_days=['Monday'],
            food_pref='Veg Only',
            work_pref='Any Family',
            status='Available',
            username='editable_helper',
            password='stored-secret',
            verification_status=Helper.VERIFICATION_STATUS_VERIFIED,
        )
        self.client.force_login(user)

        image_buffer = BytesIO()
        Image.new('RGB', (1, 1), color='blue').save(image_buffer, format='PNG')
        image_buffer.seek(0)

        with tempfile.TemporaryDirectory() as media_root:
            with self.settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    reverse('helpers:profile'),
                    {
                        'age': '35',
                        'phone': '9876543210',
                        'email': 'updated@example.com',
                        'marital_status': 'Married',
                        'children': '2',
                        'skills': 'cleaning, cooking',
                        'work_time': '9 AM - 3 PM',
                        'working_days': ['Tuesday', 'Thursday'],
                        'food_pref': 'Both',
                        'work_pref': 'Family with kids',
                        'status': 'Busy',
                        'photo': SimpleUploadedFile(
                            'profile.png',
                            image_buffer.getvalue(),
                            content_type='image/png',
                        ),
                    },
                )

                self.assertEqual(response.status_code, 302)
                self.assertRedirects(response, reverse('helpers:profile'))
                helper.refresh_from_db()
                self.assertEqual(helper.age, 35)
                self.assertEqual(helper.phone, '9876543210')
                self.assertEqual(helper.email, 'updated@example.com')
                self.assertEqual(helper.marital_status, 'Married')
                self.assertEqual(helper.children, 2)
                self.assertEqual(helper.skills, 'cleaning, cooking')
                self.assertEqual(helper.work_time, '9 AM - 3 PM')
                self.assertEqual(helper.working_days, ['Tuesday', 'Thursday'])
                self.assertEqual(helper.food_pref, 'Both')
                self.assertEqual(helper.work_pref, 'Family with kids')
                self.assertEqual(helper.status, 'Busy')
                self.assertTrue(helper.photo)

                photo_response = self.client.get(reverse('helpers:profile_photo'))
                self.assertEqual(photo_response.status_code, 200)
                self.assertEqual(photo_response['Content-Type'], 'image/png')
                photo_response.close()

                profile_response = self.client.get(reverse('helpers:profile'))
                self.assertContains(
                    profile_response,
                    reverse('helpers:profile_photo'),
                )

    def test_unverified_helper_is_shown_waiting_page_on_dashboard(self):
        user = User.objects.create_user(username='pending_dashboard_helper', password='secret123')
        Helper.objects.create(
            name='Pending Dashboard Helper',
            age=30,
            phone='1234567892',
            gender='Female',
            address='Main Street',
            pincode='560001',
            marital_status='Single',
            children=0,
            skills='cleaning',
            work_time='10 AM - 5 PM',
            food_pref='Veg Only',
            work_pref='Any Family',
            status='Available',
            username='pending_dashboard_helper',
            password=user.password,
            approved=True,
            verification_status=Helper.VERIFICATION_STATUS_PENDING,
        )
        self.client.force_login(user)

        response = self.client.get(reverse('helpers:list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'waiting.html')


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
