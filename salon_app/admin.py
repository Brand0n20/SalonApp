from django.contrib import admin
from .models import Customer, Appointment, Service, Employee, Payment

# this page registers models so they can be managed through Django's built-in admin site
admin.site.register(Customer)
admin.site.register(Appointment)
admin.site.register(Service)
admin.site.register(Employee)
admin.site.register(Payment)
