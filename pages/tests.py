from django.core import mail
from django.contrib import admin
from django.test import override_settings
from django.test import TestCase

from .admin import ContactAdmin
from .models import Contact


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class ContactReplyEmailTests(TestCase):
	def test_saving_new_reply_sends_email_and_marks_contact_replied(self):
		contact = Contact.objects.create(
			name='Test User',
			email='test@example.com',
			problem='I need help.',
		)
		contact.reply = 'Here is the answer.'
		admin_instance = ContactAdmin(Contact, admin.site)

		admin_instance.save_model(None, contact, None, True)

		contact.refresh_from_db()
		self.assertTrue(contact.replied)
		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].to, ['test@example.com'])
		self.assertIn('Here is the answer.', mail.outbox[0].body)

	def test_saving_reply_does_not_fail_when_email_delivery_is_unavailable(self):
		contact = Contact.objects.create(
			name='Test User',
			email='test@example.com',
			problem='I need help.',
		)
		contact.reply = 'Here is the answer.'
		admin_instance = ContactAdmin(Contact, admin.site)

		with override_settings(
			EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
			EMAIL_HOST='invalid.example.com',
			EMAIL_PORT=587,
		):
			admin_instance.save_model(None, contact, None, True)

		contact.refresh_from_db()
		self.assertTrue(contact.replied)
