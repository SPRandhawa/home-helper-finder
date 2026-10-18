from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Helper


@login_required(login_url='/accounts/start/helper/')
def list_helpers(request):
	helper = Helper.objects.filter(username=request.user.get_username()).first()
	if (
		helper is None
		or helper.verification_status != Helper.VERIFICATION_STATUS_VERIFIED
	):
		return render(request, 'waiting.html')

	account_details = [
		('Name', helper.name),
		('Username', helper.username),
		('Phone', helper.phone),
		('Email', helper.email),
		('Pincode', helper.pincode),
		('Skills', helper.skills),
		('Availability', helper.status),
		('Verification', helper.get_verification_status_display()),
	]

	return render(request, 'app_dashboard.html', {
		'active_page': 'helpers',
		'eyebrow': 'Helper directory',
		'heading': 'Find trusted home helpers',
		'intro': 'Browse verified profiles and discover support that fits your household.',
		'account_details': account_details,
		'actions': [
			{'label': 'Create a request', 'url_name': 'requests:create'},
			{'label': 'My account', 'url_name': 'accounts:dashboard'},
		],
	})
