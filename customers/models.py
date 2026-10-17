from django.db import models

class Helper(models.Model):
    VERIFICATION_STATUS_PENDING = 'pending'
    VERIFICATION_STATUS_VERIFIED = 'verified'
    VERIFICATION_STATUS_REJECTED = 'rejected'
    
    VERIFICATION_STATUS_CHOICES = [
        (VERIFICATION_STATUS_PENDING, 'Pending'),
        (VERIFICATION_STATUS_VERIFIED, 'Verified'),
        (VERIFICATION_STATUS_REJECTED, 'Rejected'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=20, blank=True)
    children = models.PositiveIntegerField(default=0, blank=True)
    email = models.EmailField(blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True)
    work_time = models.CharField(max_length=100, blank=True)
    food_pref = models.CharField(max_length=50, blank=True)
    work_pref = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, default='Active')
    password = models.CharField(max_length=128)
    
    approved = models.BooleanField(default=False)
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_STATUS_CHOICES, default=VERIFICATION_STATUS_PENDING)
    verification_notes = models.TextField(blank=True)
    verified_by = models.CharField(max_length=100, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    # Document Uploads
    photo = models.ImageField(upload_to='helpers/photos/', blank=True, null=True)
    latest_photo = models.ImageField(upload_to='helpers/latest_photos/', blank=True, null=True)
    aadhaar_front = models.ImageField(upload_to='helpers/documents/', blank=True, null=True)
    aadhaar_back = models.ImageField(upload_to='helpers/documents/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"
