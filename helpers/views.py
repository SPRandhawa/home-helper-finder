from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='/accounts/start/helper/')
def list_helpers(request):
	return render(request, 'app_dashboard.html', {
		'active_page': 'helpers',
		'eyebrow': 'Helper directory',
		'heading': 'Find trusted home helpers',
		'intro': 'Browse verified profiles and discover support that fits your household.',
		'actions': [
			{'label': 'Create a request', 'url_name': 'requests:create'},
			{'label': 'My account', 'url_name': 'accounts:dashboard'},
		],
	})
