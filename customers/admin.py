from django.contrib import admin
from django.utils.html import format_html
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'occupation', 'phone', 'pincode', 'username', 'photo_preview')
    search_fields = ('name', 'username', 'phone', 'email', 'occupation', 'pincode')
    readonly_fields = ('photo_preview', 'latest_photo_preview', 'aadhaar_front_preview', 'aadhaar_back_preview')

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

    @staticmethod
    def _preview_image(field):
        if not field:
            return 'No file uploaded'
        return format_html('<a href="{}" target="_blank"><img src="{}" width="80" height="80" style="object-fit:cover;" /></a>', field.url, field.url)
