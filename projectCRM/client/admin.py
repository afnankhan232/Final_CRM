from django.contrib import admin
from .models import Client
from .models import Project
from .models import Contact

# Importing Leads model(/table) from model.py
from .models import Lead

# Registering Leads model - access from admin page (@developmentSite)
admin.site.register(Lead)

# Register your models here.
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Contact)