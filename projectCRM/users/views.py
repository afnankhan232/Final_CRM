from django.shortcuts import render
from django.http import HttpResponse

allCompanies = [
	{
		'company' : "TESLA",
		'No of Employees' : 50,
		'clients': range(100),
		'active clients': range(10, 90, 2),
	},

	{
		'company' : "Salesforce",
		'No of Employees' : 390,
		'clients': range(1000),
		'active clients': range(77, 906, 7),
	},
]

# Create your views here.
def login(request, **kwargs):
	return render(
		request,
		'users/login.html',
	)

def home(request, **kwargs):
	context = {
		'companies': allCompanies,
		'current_login': allCompanies[1],
	}
	return render(
		request, 
		'users/home.html', 
		context=context,
	)

def about(request, **kwargs):
	return render(
		request,
		'users/about.html',
		context={}
	)
