from django.urls import path
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from . import views

app_name = 'helpers'

urlpatterns = [
    path('', views.list_helpers, name='list'),
    path('profile/', views.helper_profile, name='profile'),
    path('profile/photo/', views.profile_photo, name='profile_photo'),
    path(
        'password-change/',
        PasswordChangeView.as_view(
            template_name='helpers/password_change_form.html',
            success_url=reverse_lazy('helpers:profile'),
        ),
        name='password_change',
    ),
]
