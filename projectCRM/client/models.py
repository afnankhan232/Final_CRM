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