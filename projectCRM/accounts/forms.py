from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import BusinessUser

class CompanyUserCreationForm(UserCreationForm):
    class Meta:
        model = BusinessUser
        fields = (
            'company_name', 
            'company_email',
            'website', 
            'industry', 
            'employees', 
            'phone', 
            'country',
            'address',
        )