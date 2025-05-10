from django.contrib import admin
from .models import Client
from .models import Project
from .models import Document
from .models import Contact
from .models import ProjectAccessPermission
from .models import Task
from .models import ActivityLog

# Importing Leads model(/table) from model.py
from .models import Lead

# Registering Leads model - access from admin page (@developmentSite)
admin.site.register(Lead)

# Registering Document model - access from admin page (@developmentSite)
admin.site.register(Document)

# Register your models here.
admin.site.register(Client)

admin.site.register(Project)

admin.site.register(Contact)

admin.site.register(ProjectAccessPermission)

admin.site.register(Task)

admin.site.register(ActivityLog)