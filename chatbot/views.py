from django.shortcuts import render

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
