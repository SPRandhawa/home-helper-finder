import json
import re

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import ChatbotQuestion


def normalize_question(question):
	return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', question.lower())).strip()[:500]

def home(request):
	return render(request, 'app_dashboard.html', {
		'active_page': 'chatbot',
		'eyebrow': 'Home Helper assistant',
		'heading': 'A helpful place to start',
		'intro': 'Ask common questions about finding helpers, sending requests, and using the platform.',
		'actions': [
			{'label': 'Browse helpers', 'url_name': 'helpers:list'},
			{'label': 'Read the help guide', 'url_name': 'pages:help'},
		],
	})


@require_POST
def answer(request):
	try:
		payload = json.loads(request.body)
	except (json.JSONDecodeError, UnicodeDecodeError):
		return JsonResponse({'error': 'Invalid request.'}, status=400)

	question = str(payload.get('question', '')).strip()
	normalized_question = normalize_question(question)
	if not normalized_question:
		return JsonResponse({'error': 'Question is required.'}, status=400)

	chatbot_question = ChatbotQuestion.objects.filter(
		normalized_question=normalized_question,
	).first()
	if chatbot_question and chatbot_question.answer.strip():
		return JsonResponse({'answer': chatbot_question.answer, 'known': True})

	if chatbot_question is None:
		ChatbotQuestion.objects.create(
			question=question,
			normalized_question=normalized_question,
		)

	return JsonResponse({
		'answer': 'I do not know that yet. I have sent your question to our team, and they will add an answer soon.',
		'known': False,
	})
