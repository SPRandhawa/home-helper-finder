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

	return render(request, 'helpers/dashboard.html')
