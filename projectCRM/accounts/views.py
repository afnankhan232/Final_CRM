from django.shortcuts import render, redirect

from .forms import CompanyUserCreationForm

from django.contrib.auth.models import User

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Index or Home page for CRM Software
def indexView(request, *args, **kwargs):
    print(request.path)
    return render(request, 'accounts/index.html')

# About Page of CRM Software Include info about the Authors
def aboutView(request, *args, **kwargs):
    return render(request, 'accounts/about.html')

# Register a New Account
def registrationView(request, *args, **kwargs):
    if(request.method == "POST"):
        form = CompanyUserCreationForm(request.POST)
        if(form.is_valid()):
            form.save()
            companyName = form.cleaned_data.get("company_email")
            messages.success(request, f"Your account has been created! You can now log in")
            return redirect('login')
    else:
        form = CompanyUserCreationForm()
    
    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)

# Login and Logout are handled from URL-Patterns Using default django Class.

# Profile View Extends featuredApp/base.html
@login_required
def profileView(request, *args, **kwargs):
    return render(request, 'accounts/profile.html')