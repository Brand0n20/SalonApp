from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_list, name='services'),
    path('appointments/book_appointment/', views.book_appointment, name='book_appointment'),
    path('appointments', views.appointments, name='appointments'),
    path('customers/', views.customers_list, name='customers_list'),
    path('customer/<int:customer_id>/', views.customer_profile, name='customer'),

    # Authentication
    path('register/', views.register_customer, name='register_customer'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
    path('dashboard/employee/', views.employee_dashboard, name='employee_dashboard'),
]
