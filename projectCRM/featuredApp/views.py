from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def profile(request, *args, **kwargs):
    return render(request, 'users/profile.html')

@login_required
def home_view(request, *args, **kwargs):
    return render(request, 'featuredApp/home.html')

@login_required
def tasks_view(request, *args, **kwargs):
    return render(request, 'featuredApp/tasks.html')

@login_required
def activities_view(request, *args, **kwargs):
    return render(request, 'featuredApp/activities.html')

@login_required
def contact_view(request, *args, **kwargs):
    return render(request, 'featuredApp/contacts.html')