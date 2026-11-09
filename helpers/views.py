import mimetypes

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render

from .forms import HelperProfileForm
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


@login_required(login_url='/accounts/start/helper/')
def helper_profile(request):
	helper = Helper.objects.filter(username=request.user.get_username()).first()
	if (
		helper is None
		or helper.verification_status != Helper.VERIFICATION_STATUS_VERIFIED
	):
		return render(request, 'waiting.html')

	if request.method == 'POST':
		form = HelperProfileForm(request.POST, request.FILES, instance=helper)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your profile has been updated.')
			return redirect('helpers:profile')
	else:
		form = HelperProfileForm(instance=helper)

	try:
		photo_available = bool(helper.photo and helper.photo.storage.exists(helper.photo.name))
	except OSError:
		photo_available = False

	return render(request, 'helpers/profile.html', {
		'helper': helper,
		'form': form,
		'photo_available': photo_available,
	})


@login_required(login_url='/accounts/start/helper/')
def profile_photo(request):
	helper = Helper.objects.filter(
		username=request.user.get_username(),
		verification_status=Helper.VERIFICATION_STATUS_VERIFIED,
	).first()
	if helper is None or not helper.photo:
		raise Http404

	try:
		photo_file = helper.photo.open('rb')
	except (FileNotFoundError, OSError):
		raise Http404

	return FileResponse(
		photo_file,
		content_type=mimetypes.guess_type(helper.photo.name)[0] or 'application/octet-stream',
	)
