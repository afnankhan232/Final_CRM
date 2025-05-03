# ---- ==== IMPORT STATEMENT GOES HERE ==== ----

# Basic
from django.shortcuts import render, redirect

# User MODEL - Authentication and Authorization
from django.contrib.auth.models import User

# A helper notification section, which notify the new activity
from django.contrib import messages

# The Decorator, which allow the views to be accessed by only the login members
from django.contrib.auth.decorators import login_required


# ---- ==== VIEWS FILES GOES HERE ==== ----

# Index or Home page for CRM Software
def indexView(request, *args, **kwargs):
    print(request.path)
    return render(request, 'accounts/index.html')

# About Page of CRM Software Include info about the Authors
def aboutView(request, *args, **kwargs):
    return render(request, 'accounts/about.html')
