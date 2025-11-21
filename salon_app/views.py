from .models import Customer, Appointment, Service, Employee, Payment
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CustomerRegistrationForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def home(request):
    return render(request, 'salon_app/home.html')

def services_list(request):
    services = Service.objects.all()
    return render(request, 'salon_app/services_list.html', {'services': services})

@login_required
def book_appointment(request):
    if request.method == "POST":
        # Get selected service
        service_id = request.POST.get("service")
        service = Service.objects.get(id=service_id)

        # Get selected date and time
        date = request.POST.get("date")  # format: 'YYYY-MM-DD'
        time = request.POST.get("time")  # format: 'HH:MM'

        # Combine date and time into a datetime object
        from datetime import datetime
        appointment_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        # Choose an employee (example: first available)
        employee = Employee.objects.first()  # you can later add availability logic

        # Create appointment
        Appointment.objects.create(
            customer=request.user.customer,  # assuming user has customer profile
            employee=employee,
            service=service,
            appointment_date=appointment_datetime
        )

        # Redirect to customer dashboard or appointments page
        return redirect('customer_dashboard')

    else:
        # GET request: show form with all active services
        services = Service.objects.all()
        return render(request, 'salon_app/book_appointment.html', {'services': services})

@login_required
def appointments(request):
    user = request.user

    # Case 1: Logged in as customer
    if hasattr(user, 'customer'):
        appts = Appointment.objects.filter(customer=user.customer, status='Scheduled')

    # Case 2: Logged in as employee
    elif hasattr(user, 'employee'):
        appts = Appointment.objects.filter(employee=user.employee, status='Scheduled')

    # Case 3: User has neither profile
    else:
        return HttpResponseForbidden("No associated profile found.")

    return render(request, 'salon_app/appointments.html', {
        'appointments': appts
    })

@login_required
def cancel_appointment(request, appointment_id):
    # Get the appointment
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Ensure the user is allowed to cancel it
    if hasattr(request.user, 'customer') and appointment.customer != request.user.customer:
        return HttpResponseForbidden("You cannot cancel someone else's appointment.")
    if hasattr(request.user, 'employee') and appointment.employee != request.user.employee:
        return HttpResponseForbidden("You cannot cancel someone else's appointment.")

    # Update status to Cancelled
    appointment.status = "Cancelled"
    appointment.save()

    # Redirect back to dashboard or appointments page
    if hasattr(request.user, 'customer'):
        return redirect('customer_dashboard')
    else:
        return redirect('employee_dashboard')


def customer_profile(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    appointments = Appointment.objects.filter(customer=customer)
    return render(request, 'salon_app/customer_profile.html', {
        'customer': customer,
        'appointments': appointments
    })

def customers_list(request):
    if not request.user.is_staff:
        return {HttpResponseForbidden("You do not have permission to view this page")}
    
    customers = Customer.objects.all()
    return render(request, 'salon_app/customer_list.html', {'customers': customers})

def register_customer(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            customer = form.save()
            login(request, customer.user)
    else:
        form = CustomerRegistrationForm()
    return render(request, 'salon_app/register_customer.html', {'form': form})

def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST['username']  # email is the username
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # If employee has profile:
            if hasattr(user, 'employee'):
                return redirect('employee_dashboard')

            # If customer has profile:
            if hasattr(user, 'customer'):
                return redirect('customer_dashboard')

            return redirect('home')

        else:
            error = "Invalid username or password"

    return render(request, 'salon_app/login.html', {"error": error})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def customer_dashboard(request):
    # Ensure this user has a customer profile
    if not hasattr(request.user, 'customer'):
        return redirect('login')

    customer = request.user.customer
    appointments = Appointment.objects.filter(customer=customer, status='Scheduled')

    return render(request, 'salon_app/customer_dashboard.html', {
        'customer': customer,
        'appointments': appointments
    })


@login_required
def employee_dashboard(request):
    # Ensure this user has an employee profile
    if not hasattr(request.user, 'employee'):
        return redirect('login')

    employee = request.user.employee

    return render(request, 'salon_app/employee_dashboard.html', {
        'employee': employee
    })