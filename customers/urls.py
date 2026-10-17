from django.urls import path

from . import views

app_name = 'customers'

urlpatterns = [
    path('login/customer/', views.login_customer_view, name='login_customer'),
]
