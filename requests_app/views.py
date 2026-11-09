from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from helpers.models import Helper

from .forms import ServiceRequestForm
from .models import ServiceRequest


def _verified_helper_for(user):
    return Helper.objects.filter(
        username=user.get_username(),
        verification_status=Helper.VERIFICATION_STATUS_VERIFIED,
    ).first()


@login_required(login_url='/accounts/start/customer/')
def request_list(request):
    if Helper.objects.filter(username=request.user.get_username()).exists():
        return HttpResponseForbidden('Helper accounts should use the helper dashboard.')
    requests = ServiceRequest.objects.filter(customer=request.user).select_related('helper')
    return render(request, 'requests_app/list.html', {'service_requests': requests})


@login_required(login_url='/accounts/start/customer/')
def create_request(request):
    if Helper.objects.filter(username=request.user.get_username()).exists():
        return HttpResponseForbidden('Only customer accounts can create service requests.')

    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            messages.success(request, 'Your request was sent to available helpers.')
            return redirect('requests:list')
    else:
        form = ServiceRequestForm(user=request.user)

    return render(request, 'requests_app/create.html', {'form': form})


@login_required(login_url='/accounts/start/helper/')
@require_POST
def decide_request(request, request_id, decision):
    helper = _verified_helper_for(request.user)
    if helper is None:
        return HttpResponseForbidden('A verified helper account is required.')
    if decision not in {'accept', 'reject'}:
        return HttpResponseForbidden('Invalid request action.')

    service_request = get_object_or_404(
        ServiceRequest,
        pk=request_id,
        status=ServiceRequest.STATUS_PENDING,
        helper__isnull=True,
    ).exclude(rejected_by=helper)

    if decision == 'accept':
        with transaction.atomic():
            claimed = ServiceRequest.objects.filter(
                pk=service_request.pk,
                status=ServiceRequest.STATUS_PENDING,
                helper__isnull=True,
            ).update(helper=helper, status=ServiceRequest.STATUS_ACCEPTED)
        if claimed:
            messages.success(request, 'You accepted this job request.')
        else:
            messages.warning(request, 'Another helper has already accepted this request.')
    else:
        service_request.rejected_by.add(helper)
        messages.info(request, 'This request was removed from your available jobs.')

    return redirect('helpers:list')
