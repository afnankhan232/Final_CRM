from django.shortcuts import render
from .models import Client

# Create your views here.
def clientsPageViews(request, *args, **kwargs):
    context = {
        'Clients': Clients.objects.all(),
        'checkVar': True, 
    }
    if (User.is_authenticated):
        print("is Authenticated??")
    else:
        print("Do Something")
    return render(request, 'accounts/clients.html', context)