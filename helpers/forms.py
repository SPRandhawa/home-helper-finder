from django import forms

from .models import Helper


WORKING_DAYS = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]


class HelperProfileForm(forms.ModelForm):
    photo = forms.ImageField(
        label='Profile photo',
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
    )
    marital_status = forms.ChoiceField(choices=[
        ('Single', 'Single'),
        ('Married', 'Married'),
    ])
    working_days = forms.MultipleChoiceField(
        choices=WORKING_DAYS,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    food_pref = forms.ChoiceField(choices=[
        ('Veg Only', 'Veg Only'),
        ('Non-Veg Only', 'Non-Veg Only'),
        ('Both', 'Both'),
    ])
    work_pref = forms.ChoiceField(choices=[
        ('Any Family', 'Any Family'),
        ('Family without kids', 'Family without kids'),
        ('Family with kids', 'Family with kids'),
        ('No single male', 'No single male'),
    ])
    status = forms.ChoiceField(choices=[
        ('Available', 'Available'),
        ('Busy', 'Busy'),
    ])

    class Meta:
        model = Helper
        fields = (
            'photo',
            'age',
            'phone',
            'email',
            'marital_status',
            'children',
            'skills',
            'experience',
            'work_time',
            'working_days',
            'food_pref',
            'work_pref',
            'status',
        )
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['working_days'] = self.instance.working_days
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs['class'] = (
                    'w-full rounded-lg border border-slate-300 px-3 py-2 '
                    'text-slate-900 focus:border-green focus:outline-none'
                )
        self.fields['photo'].required = False
        self.fields['email'].required = False
