from django.shortcuts import render

def dashboard(request):
	return render(request, 'app_dashboard.html', {
		'active_page': 'accounts',
		'eyebrow': 'Your account',
		'heading': 'Welcome to your account',
		'intro': 'Manage your profile and choose how you use Home Helper Finder.',
		'actions': [
			{'label': 'Find helpers', 'url_name': 'helpers:list'},
			{'label': 'View requests', 'url_name': 'requests:list'},
		],
	})
