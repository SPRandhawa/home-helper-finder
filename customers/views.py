from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='/accounts/start/customer/')
def dashboard(request):
	return render(request, 'app_dashboard.html', {
		'active_page': 'customers',
		'eyebrow': 'Customer space',
		'heading': 'Organize help for your home',
		'intro': 'Search for helpers, send requests, and keep track of your connections in one place.',
		'actions': [
			{'label': 'Find a helper', 'url_name': 'helpers:list'},
			{'label': 'New request', 'url_name': 'requests:create'},
		],
	})
