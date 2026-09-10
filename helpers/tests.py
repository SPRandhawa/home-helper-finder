from django.test import TestCase

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
