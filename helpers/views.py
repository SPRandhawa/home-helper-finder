import mimetypes

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render

from .forms import HelperProfileForm
from .models import Helper
from requests_app.models import ServiceRequest


@login_required(login_url='/accounts/start/helper/')
def list_helpers(request):
	helper = Helper.objects.filter(username=request.user.get_username()).first()
	if (
		helper is None
		or helper.verification_status != Helper.VERIFICATION_STATUS_VERIFIED
	):
		return render(request, 'waiting.html')

	skills = [skill.strip() for skill in helper.skills.split(',') if skill.strip()]
	available_requests = ServiceRequest.objects.filter(
		status=ServiceRequest.STATUS_PENDING,
		helper__isnull=True,
	).exclude(rejected_by=helper).select_related('customer').order_by('-created_at')
	accepted_jobs = ServiceRequest.objects.filter(
		helper=helper,
		status=ServiceRequest.STATUS_ACCEPTED,
	).select_related('customer').order_by('preferred_date', '-created_at')
	recent_requests = list(available_requests[:8])
	upcoming_jobs = list(accepted_jobs[:5])
	for job in recent_requests + upcoming_jobs:
		job.whatsapp_number = ''.join(char for char in (job.customer_phone or '') if char.isdigit())
		try:
			job.customer_photo_available = bool(
				job.customer_photo
				and job.customer_photo.storage.exists(job.customer_photo.name)
			)
		except OSError:
			job.customer_photo_available = False

	return render(request, 'helpers/dashboard.html', {
		'helper': helper,
		'skills': skills,
		'work_time': helper.work_time,
		'work_days': helper.working_days,
		'food_preference': helper.food_pref,
		'work_preference': helper.work_pref,
		'experience': helper.experience,
		'recent_requests': recent_requests,
		'upcoming_jobs': upcoming_jobs,
		'pending_requests': available_requests.count(),
		'accepted_jobs': accepted_jobs.count(),
	})


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
