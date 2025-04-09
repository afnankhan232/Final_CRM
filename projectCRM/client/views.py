from django.shortcuts import render
from .models import Client

# Create your views here.
def clientsPageViews(request, *args, **kwargs):
    context = {
        'Clients': Clients.objects.all(),
        'checkVar': True, 
    }
    if (request.user.is_authenticated):
        print("is Authenticated!!")
    else:
        print("Login Required! To use application")
    return render(request, 'accounts/clients.html', context)