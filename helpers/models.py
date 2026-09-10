from django.db import models


class Helper(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    phone = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    address = models.TextField()
    marital_status = models.CharField(max_length=50)
    children = models.IntegerField()
    email = models.EmailField(blank=True, null=True)
    skills = models.TextField()
    work_time = models.CharField(max_length=100)
    food_pref = models.CharField(max_length=50)
    work_pref = models.CharField(max_length=100)
    status = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    approved = models.BooleanField(default=False)

    photo = models.ImageField(upload_to='helpers/photos/', blank=True, null=True)
    latest_photo = models.ImageField(upload_to='helpers/latest_photos/', blank=True, null=True)
    aadhaar_front = models.ImageField(upload_to='helpers/aadhaar/', blank=True, null=True)
    aadhaar_back = models.ImageField(upload_to='helpers/aadhaar/', blank=True, null=True)

    def __str__(self):
        return self.name
