from django.urls import path

from . import views

app_name = 'requests'

urlpatterns = [
    path('', views.request_list, name='list'),
    path('new/', views.create_request, name='create'),
]
