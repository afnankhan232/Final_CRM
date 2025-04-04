from django.shortcuts import render

# Create your views here.
def profile(request, *args, **kwargs):
    return render(request, 'users/profile.html')