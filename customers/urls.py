from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/customer/', views.register_customer_view, name='register_customer'),
]
