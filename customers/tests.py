from django.test import TestCase
from .models import Customer

class CustomerModelTestCase(TestCase):
    def test_customer_creation(self):
        customer = Customer.objects.create(
            name="Test Customer",
            occupation="Engineer",
            phone="1234567890",
            username="testcustomer",
            pincode="110001",
            address="Test Address"
        )
        self.assertEqual(customer.name, "Test Customer")
        self.assertEqual(customer.occupation, "Engineer")
