from django.db import models
from accounts.models import CompanyUser

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    companyAssignee = models.ForeignKey(CompanyUser, on_delete=models.CASCADE)