from django.db import models
# from django.contrb.auth.models import User

class CompanyUser(models.Model):

    # Fields AbstractUser: username, password, first_name, last_name, email, etc.

    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    num_employees = models.PositiveIntegerField(default=1)
    phone = models.CharField(max_length=20, default=None)
    country = models.CharField(max_length=100, default=None)
    company_email = models.CharField(max_length=100)

# python manage.py migrate && python manage.py createsuperuser && python manage.py makemigrations && python manage.py migrate