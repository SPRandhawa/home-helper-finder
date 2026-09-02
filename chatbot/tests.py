from django.test import TestCase

from django.urls import reverse

from .models import ChatbotQuestion


class ChatbotAnswerTests(TestCase):
	def test_unknown_question_is_saved_for_admin(self):
		response = self.client.post(
			reverse('chatbot:answer'),
			data='{"question":"Can I book a helper on Sunday?"}',
			content_type='application/json',
		)

		self.assertEqual(response.status_code, 200)
		self.assertFalse(response.json()['known'])
		self.assertTrue(ChatbotQuestion.objects.filter(
			normalized_question='can i book a helper on sunday',
			answer='',
		).exists())

	def test_answered_question_returns_saved_answer(self):
		ChatbotQuestion.objects.create(
			question='Can I book a helper on Sunday?',
			normalized_question='can i book a helper on sunday',
			answer='Yes, Sunday bookings are available.',
		)

		response = self.client.post(
			reverse('chatbot:answer'),
			data='{"question":"CAN I BOOK A HELPER ON SUNDAY?"}',
			content_type='application/json',
		)

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.json()['known'])
		self.assertEqual(response.json()['answer'], 'Yes, Sunday bookings are available.')
