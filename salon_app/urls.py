from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_list, name='services'),
    path('book_appointment/', views.book_appointment, name='appointments'),
    path('customers/', views.customers_list, name='customers_list'),
    path('customer/<int:customer_id>/', views.customer_profile, name='customer'),
]
