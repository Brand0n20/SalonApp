from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_list, name='services_list'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('customer/<int:customer_id>/', views.customer_profile, name='customer_profile'),
]
