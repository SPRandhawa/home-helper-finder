from accounts.views import login_view
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def login_customers_view(request):
	return login_view(request, 'customer')


@login_required(login_url='/accounts/start/customer/')
def dashboard(request):
	return render(request, 'customers/dashboard.html')
