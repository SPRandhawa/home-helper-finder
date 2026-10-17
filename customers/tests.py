from django.test import TestCase
from .models import Helper

class HelperModelTestCase(TestCase):
    def setUp(self):
        self.helper = Helper.objects.create(
            name="Rahul Sharma",
            username="rahulsharma",
            phone="9876543210",
            pincode="110001",
            verification_status=Helper.VERIFICATION_STATUS_PENDING
        )

    def test_helper_creation(self):
        self.assertEqual(self.helper.name, "Rahul Sharma")
        self.assertEqual(self.helper.verification_status, "pending")
        self.assertFalse(self.helper.approved)
        self.assertIn("Rahul Sharma", str(self.helper))
