from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from helpers.models import Helper


@admin.register(Helper)
class HelperAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'username',
        'phone',
        'pincode',
        'verification_status',
        'approved',
        'photo_preview',
        'latest_photo_preview',
        'aadhaar_front_preview',
        'aadhaar_back_preview',
    )
    list_filter = ('verification_status', 'approved', 'gender', 'marital_status')
    search_fields = ('name', 'username', 'phone', 'email', 'pincode', 'address')
    readonly_fields = (
        'photo_preview',
        'latest_photo_preview',
        'aadhaar_front_preview',
        'aadhaar_back_preview',
    )
    actions = ['mark_verified', 'mark_rejected']

    fieldsets = (
        ('Identity', {
            'fields': (
                'name', 'age', 'phone', 'gender', 'address', 'pincode',
                'marital_status', 'children', 'email', 'skills', 'work_time',
                'food_pref', 'work_pref', 'status', 'username', 'password',
                'approved',
            )
        }),
        ('Verification', {
            'fields': (
                'verification_status', 'verification_notes', 'verified_by',
                'verified_at', 'photo_preview', 'latest_photo_preview',
                'aadhaar_front_preview', 'aadhaar_back_preview',
            )
        }),
        ('Documents', {
            'fields': ('photo', 'latest_photo', 'aadhaar_front', 'aadhaar_back')
        }),
    )

    def photo_preview(self, obj):
        return self._preview_image(obj.photo)

    photo_preview.short_description = 'Photo'

    def latest_photo_preview(self, obj):
        return self._preview_image(obj.latest_photo)

    latest_photo_preview.short_description = 'Latest Photo'

    def aadhaar_front_preview(self, obj):
        return self._preview_image(obj.aadhaar_front)

    aadhaar_front_preview.short_description = 'Aadhaar Front'

    def aadhaar_back_preview(self, obj):
        return self._preview_image(obj.aadhaar_back)

    aadhaar_back_preview.short_description = 'Aadhaar Back'

    def photo_preview(self, obj):
        return self._preview_image(obj.photo)

    def latest_photo_preview(self, obj):
        return self._preview_image(obj.latest_photo)

    def aadhaar_front_preview(self, obj):
        return self._preview_image(obj.aadhaar_front)

    def aadhaar_back_preview(self, obj):
        return self._preview_image(obj.aadhaar_back)

    @staticmethod
    def _preview_image(field):
        if not field:
            return 'No file uploaded'
        return format_html('<a href="{}" target="_blank"><img src="{}" width="80" height="80" style="object-fit:cover;" /></a>', field.url, field.url)

    @admin.action(description='Mark selected helpers as verified')
    def mark_verified(self, request, queryset):
        queryset.update(
            verification_status=Helper.VERIFICATION_STATUS_VERIFIED,
            verified_by=getattr(request.user, 'username', 'admin'),
            verified_at=timezone.now(),
        )

    @admin.action(description='Mark selected helpers as rejected')
    def mark_rejected(self, request, queryset):
        queryset.update(
            verification_status=Helper.VERIFICATION_STATUS_REJECTED,
            verified_by=getattr(request.user, 'username', 'admin'),
            verified_at=timezone.now(),
        )
