from django import forms
from django.contrib.auth.models import User
from .models import Customer

class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'password']

    def save(self, commit=True):
        # Create Django User first
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )

        # Create customer linked to user
        customer = Customer(
            user=user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            phone=self.cleaned_data['phone'],
            date_joined = self.cleaned_data['date_joined']
        )

        if commit:
            customer.save()

        return customer
