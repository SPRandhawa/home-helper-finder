from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('start/<str:destination>/', views.start, name='start'),
    path('login/<str:destination>/', views.login_view, name='login'),
    path('terms/<str:destination>/', views.terms_consent, name='terms_consent'),
    path('create-account/<str:destination>/', views.create_account, name='create_account'),
    path('', views.dashboard, name='dashboard'),
]
