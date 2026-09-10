from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect, render

from helpers.models import Helper


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
		user = form.get_user()
		login(request, user)

		if destination == 'helper':
			helper = Helper.objects.filter(username=user.username).first()
			if helper is None:
				return redirect(DESTINATIONS[destination])
			if not helper.approved:
				return render(request, 'waiting.html')
			return redirect(DESTINATIONS[destination])

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

	if request.method == 'POST' and destination == 'helper':
		username = request.POST.get('username', '').strip()
		if Helper.objects.filter(username=username).exists():
			return render(request, f'accounts/create_{destination}.html', {
				'error': 'User already exists. Please choose another username.'
			})
		if User.objects.filter(username=username).exists():
			return render(request, f'accounts/create_{destination}.html', {
				'error': 'User already exists. Please choose another username.'
			})

		password = request.POST.get('password', '')
		try:
			user = User.objects.create_user(username=username, password=password)
			Helper.objects.create(
				name=request.POST.get('name', ''),
				age=int(request.POST.get('age', 0) or 0),
				phone=request.POST.get('phone', ''),
				gender=request.POST.get('gender', ''),
				address=request.POST.get('address', ''),
				pincode=request.POST.get('pincode', ''),
				marital_status=request.POST.get('marital_status', ''),
				children=int(request.POST.get('children', 0) or 0),
				email=request.POST.get('email') or '',
				skills=request.POST.get('skills', ''),
				work_time=request.POST.get('work_time', ''),
				food_pref=request.POST.get('food_pref', ''),
				work_pref=request.POST.get('work_pref', ''),
				status=request.POST.get('status') or 'Available',
				username=username,
				password=password,
				approved=False,
				photo=request.FILES.get('photo'),
				latest_photo=request.FILES.get('latest_photo'),
				aadhaar_front=request.FILES.get('aadhaar_front'),
				aadhaar_back=request.FILES.get('aadhaar_back'),
			)
			return render(request, 'waiting.html')
		except IntegrityError:
			return render(request, f'accounts/create_{destination}.html', {
				'error': 'User already exists. Please choose another username.'
			})

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
