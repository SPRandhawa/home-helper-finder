from django.urls import path

from . import views

app_name = 'customers'

urlpatterns = [
    path('login/customers/', views.login_customers_view, name='login_customers'),
]
