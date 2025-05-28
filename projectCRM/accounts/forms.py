from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import FileInput
from .models import BusinessUser
from .models import Role
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

class BusinessUserUpdationForm(forms.ModelForm):
    
    class Meta:
        model = BusinessUser
        fields = [
            'company_name',
            'company_logo',
            'industry',
            'job_title',
            'employees',
            'website',
            'address',
            'country',
            'phone',
        ]

        widget = {
            'company_logo': FileInput(),
        }
    
class RolesCreationForm_Account(forms.ModelForm):
    class Meta:
        model = Role
        fields = [
            'name',
            # Contacts
            'can_read_contact', 'can_add_contact', 'can_edit_contact',
            'can_delete_contact', 'can_permanent_delete_contact',

            # Projects
            'can_add_project',

            # Tasks
            'can_read_tasks', 'can_add_tasks', 'can_edit_tasks',
            'can_delete_tasks', 'can_permanent_delete_tasks',

            # Documents
            'can_read_documents', 'can_add_documents', 'can_edit_documents',
            'can_delete_documents', 'can_permanent_delete_documents',
        ]
        widgets = {
            field: forms.CheckboxInput(attrs={'class': 'form-check-input'})
            for field in fields if field != 'name'
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # fallback to None
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter role name'
        })
    
    # Since we need the name of the each form to be unique for a user
    # we need to over-ride the [clean] method
    # It prevent from unusual error page
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Role.objects.filter(name=name, user=self.user).exists():
            raise forms.ValidationError("You already have a Role with this name.")
        return name


class AccessShareForm(forms.Form):
    shared_with_emails = forms.CharField(widget=forms.HiddenInput(), required=False)

from django import forms

class FeedbackForm(forms.Form):
    description = forms.CharField(
        label="Your Feedback",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Share your thoughts...',
            'rows': 3,
        })
    )
    allow_contact = forms.BooleanField(
        required=False,
        label="Allow us to reach out via email",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )