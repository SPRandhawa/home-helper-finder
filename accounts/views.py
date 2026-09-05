from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


DESTINATIONS = {
	'customer': 'customers:dashboard',
	'helper': 'helpers:list',
}


def _destination_data(destination):
	if destination not in DESTINATIONS:
		return None
	return {
		'name': 'Customer Space' if destination == 'customer' else 'Helper Space',
		'url': DESTINATIONS[destination],
	}


def start(request, destination):
	destination_data = _destination_data(destination)
	if destination_data is None:
		return redirect('pages:home')
	if request.user.is_authenticated:
		return redirect(destination_data['url'])
	return render(request, 'accounts/start.html', {
		'destination': destination,
		'destination_name': destination_data['name'],
	})


def login_view(request, destination):
	destination_data = _destination_data(destination)
	if destination_data is None:
		return redirect('pages:home')
	form = AuthenticationForm(request, data=request.POST or None)
	if request.method == 'POST' and form.is_valid():
		login(request, form.get_user())
		return redirect(destination_data['url'])
	return render(request, 'accounts/login.html', {
		'form': form,
		'destination': destination,
		'destination_name': destination_data['name'],
	})


def terms_consent(request, destination):
	destination_data = _destination_data(destination)
	if destination_data is None:
		return redirect('pages:home')
	if request.method == 'POST' and request.POST.get('terms_agreement') == 'on':
		request.session[f'signup_consent_{destination}'] = True
		return redirect('accounts:create_account', destination=destination)
	return render(request, 'accounts/consent.html', {
		'auth_flow': True,
		'destination': destination,
		'destination_name': destination_data['name'],
		'consent_error': request.method == 'POST',
	})


def create_account(request, destination):
	destination_data = _destination_data(destination)
	if destination_data is None:
		return redirect('pages:home')
	if not request.session.get(f'signup_consent_{destination}'):
		return redirect('accounts:terms_consent', destination=destination)
	return render(request, f'accounts/create_{destination}.html')

@login_required(login_url='/accounts/start/customer/')
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
