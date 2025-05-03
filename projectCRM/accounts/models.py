from django.db import models
from django.contrib.auth.models import User

def get_image_filepath(self, filename):
    return f'company_logos/{str(self.pk)}/{"logo.png"}'

def get_default_image():
    return f'company_logos/default/logo.png'

class BusinessUser(models.Model):
    
    company_email = models.EmailField(max_length=60, unique=True, null=True, blank=True)
    company_name = models.CharField(max_length=95, unique=True, null=True, blank=True)

    industry = models.CharField(max_length=100, blank=True, null=True)

    job_title = models.CharField(max_length=255, blank=True, null=True)
    employees = models.IntegerField(default=None, blank=True, null=True)

    website = models.URLField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    country = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    last_login = models.DateTimeField(auto_now=True)

    company_logo = models.ImageField(upload_to=get_image_filepath, blank=True, null=True, default=get_default_image)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.company_email} - {self.company_name}"

    def get_logo_filename(self):
        return str(self.company_logo)[str(self.company_logo).index(f'company_logos/{self.pk}/'):]

# python manage.py migrate && python manage.py createsuperuser && python manage.py makemigrations && python manage.py migrate