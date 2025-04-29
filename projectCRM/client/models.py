from django.db import models
from accounts.models import BusinessUser

# Leads Model
# - INCLUDE (priority, status, name, email, description, created_at, created_by)
class Lead(models.Model):

    # simplifying work for form creation
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    # included at the priority (choices)
    CHOICE_PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )

    # Simplifying work for form creation
    NEW = 'new'
    CONTACTED = 'contacted'
    WON = 'won'
    LOST = 'lost'

    # included at the set of choices @status
    CHOICES_STATUS = (
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (WON, 'Won'),
        (LOST, 'Lost'),
    )

    # Based on Current Software (these fields are needed)
    priority = models.CharField(max_length=10, choices=CHOICE_PRIORITY, default=MEDIUM)
    status =  models.CharField(max_length=10, choices=CHOICES_STATUS, default=NEW)

    # Important Info 
    name = models.CharField(max_length=255)
    email = models.EmailField()

    # Exceptional Field
    description = models.TextField(blank = True, null = True)

    # Linking with the BusinessUser Model (every current authenticated user have their own specified leads)
    created_by = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)

    # Just acquiring more information (can be used for data analysis*)
    created_at = models.DateTimeField(auto_now_add = True)
    modified_at = models.DateTimeField(auto_now = True)


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    is_active = models.BooleanField(default=True)
    companyAssignee = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)

class Project(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)

class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)