from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Customer(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    pincode = models.CharField(max_length=10)
    address = models.TextField()
    marital_status = models.CharField(max_length=20)
    children = models.PositiveIntegerField(default=0)
    email = models.EmailField(blank=True, null=True)

    # Documents & Photos
    photo = models.ImageField(upload_to='customers/photos/')
    latest_photo = models.ImageField(upload_to='customers/latest_photos/')
    aadhaar_front = models.ImageField(upload_to='customers/documents/')
    aadhaar_back = models.ImageField(upload_to='customers/documents/')

    # Login Details
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)

    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.occupation})"
