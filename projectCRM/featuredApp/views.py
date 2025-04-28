from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from client.models import Contact, Project

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
    user = request.user
    contacts = Contact.objects.filter(owner=user)
    projects = Project.objects.filter(user=user)
    return render(request, 'featuredApp/contacts.html', {
        'contacts': contacts,
        'projects': projects,
        'total_contacts': contacts.count()
    })