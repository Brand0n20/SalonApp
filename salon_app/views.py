from .models import Customer, Appointment, Service, Employee, Payment
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CustomerRegistrationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'salon_app/home.html')

def services_list(request):
    services = Service.objects.all()
    return render(request, 'salon_app/services_list.html', {'services': services})

@login_required
def book_appointment(request):
    # Logged-in User → Customer object
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        return render(request, "salon_app/error.html", {
            "message": "You must be a customer to book appointments."
        })

    services = Service.objects.all()
    employees = Employee.objects.all()

    if request.method == "POST":
        service_id = request.POST.get("service")
        employee_id = request.POST.get("employee")
        date = request.POST.get("appointment_date")

        if not (service_id and employee_id and date):
            return render(request, "salon_app/book_appoinment.html", {
                "services": services,
                "employees": employees,
                "error": "All fields are required."
            })

        service = Service.objects.get(id=service_id)
        employee = Employee.objects.get(id=employee_id)

        Appointment.objects.create(
            customer=customer,
            employee=employee,
            service=service,
            appointment_date=date,
        )

        return redirect("customer_dashboard")  # Make sure this exists

    return render(request, "salon_app/book_appoinment.html", {
        "services": services,
        "employees": employees
    })

@login_required
def appointments(request):
    user = request.user

    # Case 1: Logged in as customer
    if hasattr(user, 'customer'):
        appts = Appointment.objects.filter(customer=user.customer)

    # Case 2: Logged in as employee
    elif hasattr(user, 'employee'):
        appts = Appointment.objects.filter(employee=user.employee)

    # Case 3: User has neither profile
    else:
        return HttpResponseForbidden("No associated profile found.")

    return render(request, 'salon_app/appointments.html', {
        'appointments': appts
    })


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
    appointments = Appointment.objects.filter(customer=customer)

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