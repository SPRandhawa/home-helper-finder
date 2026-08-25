from django.urls import path

from . import views

app_name = 'helpers'

urlpatterns = [
    path('', views.list_helpers, name='list'),
]
