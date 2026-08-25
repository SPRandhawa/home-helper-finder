from django.shortcuts import render

def request_list(request):
	return render(request, 'app_dashboard.html', {
		'active_page': 'requests',
		'eyebrow': 'Service requests',
		'heading': 'Your requests, clearly tracked',
		'intro': 'This space will keep conversations and request status together as the platform grows.',
		'actions': [
			{'label': 'Find helpers', 'url_name': 'helpers:list'},
			{'label': 'Ask the assistant', 'url_name': 'chatbot:home'},
		],
	})


def create_request(request):
	return render(request, 'app_dashboard.html', {
		'active_page': 'requests',
		'eyebrow': 'New request',
		'heading': 'Start a service request',
		'intro': 'Request creation is ready for the next model and form step. Begin by browsing available helpers.',
		'actions': [{'label': 'Browse helpers', 'url_name': 'helpers:list'}],
	})
