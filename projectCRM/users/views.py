from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request, **kwargs):
	return render(
		request, 
		'users/home.html', 
		context={}
	)

def about(request, **kwargs):
	return HttpResponse("This is an Updated Page")