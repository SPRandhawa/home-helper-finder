from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/customer/', views.register_customer_view, name='register_customer'),
]
