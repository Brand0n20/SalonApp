from .models import Customer, Appointment, Service, Employee, Payment
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

def home(request):
    return HttpResponse("<h1>Welcome to Reimagined Studio!</h1")

def services_list(request):
    services = Service.objects.all()
    return render(request, 'salon_app/services_list.html', {'services': services})

def book_appointment(request):
    return render(request, 'salon_app/book_appointment.html')

def customer_profile(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    appointments = Appointment.objects.filter(customer=customer)
    return render(request, 'salon_app/customer_profile.html', {
        'customer': customer,
        'appointments': appointments
    })

def customers_list(request):
    customers = Customer.objects.all()
    return render(request, 'salon_app/customer_list.html', {'customers': customers})