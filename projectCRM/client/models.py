from django.db import models
from accounts.models import BusinessUser

# Create your models here.
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