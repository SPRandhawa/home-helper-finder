from django import forms

from .models import ServiceRequest


class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = (
            'customer_name',
            'customer_phone',
            'customer_photo',
            'address',
            'service_type',
            'details',
            'preferred_date',
            'preferred_time',
        )
        widgets = {
            'customer_name': forms.TextInput(attrs={'autocomplete': 'name'}),
            'customer_phone': forms.TelInput(attrs={
                'autocomplete': 'tel',
                'placeholder': '+country code and phone number',
            }),
            'customer_photo': forms.FileInput(attrs={'accept': 'image/*'}),
            'address': forms.Textarea(attrs={'rows': 3, 'autocomplete': 'street-address'}),
            'details': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe the work, home size, schedule, and any important requirements.',
            }),
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'preferred_time': forms.TextInput(attrs={'placeholder': 'For example, weekdays 9 AM–1 PM'}),
        }
        labels = {
            'customer_phone': 'Phone number (include country code for WhatsApp)',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['customer_name'].initial = user.get_full_name() or user.get_username()
            self.fields['customer_phone'].initial = getattr(user, 'phone', '')
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 '
                'focus:border-green focus:outline-none',
            )
