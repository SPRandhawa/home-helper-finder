from django.conf import settings
from django.db import models

from helpers.models import Helper


class ServiceRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    SERVICE_CHOICES = [
        ('maid', 'House cleaning / Maid'),
        ('cooking', 'Cooking'),
        ('babysitting', 'Babysitting'),
        ('elder_care', 'Elder care'),
        ('pet_care', 'Pet care'),
        ('other', 'Other home help'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='service_requests',
    )
    helper = models.ForeignKey(
        Helper,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='service_requests',
    )
    rejected_by = models.ManyToManyField(
        Helper,
        blank=True,
        related_name='rejected_service_requests',
    )
    customer_name = models.CharField(max_length=150)
    customer_phone = models.CharField(max_length=30)
    customer_photo = models.ImageField(
        upload_to='service_requests/customers/', blank=True, null=True,
    )
    address = models.TextField()
    service_type = models.CharField(max_length=30, choices=SERVICE_CHOICES)
    details = models.TextField()
    preferred_date = models.DateField(blank=True, null=True)
    preferred_time = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.get_service_type_display()} for {self.customer_name}'
