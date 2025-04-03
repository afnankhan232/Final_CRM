from django.shortcuts import render, redirect

from .forms import UserRegisterForm

from django.contrib.auth.models import User

from django.contrib import messages

# Create your views here.
def registrationView(request, *args, **kwargs):
    if(request.method == "POST"):
        form = UserRegisterForm(request.POST)
        if(form.is_valid()):
            companyName = form.cleaned_data.get("company_email")
            messages.success(request, f"Account is Created!")
            return redirect('home')
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)

def accountsViews(request, *args, **kwargs):
    return render(request, 'accounts/home.html')