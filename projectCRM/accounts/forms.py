from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BusinessUser

class CompanyUserCreationForm(UserCreationForm):

    website = forms.URLField(required=False)
    industry = forms.CharField(max_length=255, required=False)
    employees = forms.IntegerField(required=False)
    phone = forms.CharField(max_length=20, required=False)
    country = forms.CharField(max_length=100, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 
                  'website', 'industry', 
                  'employees', 'phone', 'country', 'address']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            BusinessUser.objects.update_or_create(
                user=user,
                defaults = {
                    'company_name' : self.cleaned_data['username'],
                    'company_email' : self.cleaned_data['email'],
                    'website' : self.cleaned_data['website'],
                    'industry' : self.cleaned_data['industry'],
                    'employees' : self.cleaned_data['employees'],
                    'phone' : self.cleaned_data['phone'],
                    'country' : self.cleaned_data['country'],
                    'address' : self.cleaned_data['address'],
                }
            )
        return user