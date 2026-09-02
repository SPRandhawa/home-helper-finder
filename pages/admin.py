from django.contrib import admin
from django.contrib import messages
from django.core.mail import send_mail

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'replied', 'created_at')

    def save_model(self, request, obj, form, change):
        old_reply = None
        if change:
            old_reply = Contact.objects.get(pk=obj.pk).reply

        has_new_reply = bool(obj.reply and obj.reply.strip()) and obj.reply != old_reply
        if has_new_reply:
            obj.replied = True

        super().save_model(request, obj, form, change)

        if has_new_reply:
            email_sent = send_mail(
                subject='Reply from Home Helper Finder',
                message=(
                    f'Hello {obj.name},\n\n'
                    f'Thank you for contacting Home Helper Finder.\n\n'
                    f'Our team replied to your message:\n\n{obj.reply}\n\n'
                    'Regards,\nHome Helper Finder Team'
                ),
                from_email=None,
                recipient_list=[obj.email],
                fail_silently=True,
            )
            if request is not None:
                if email_sent:
                    self.message_user(request, 'Reply saved and email sent.', messages.SUCCESS)
                else:
                    self.message_user(
                        request,
                        'Reply saved, but the email could not be sent. Check the email settings.',
                        messages.WARNING,
                    )