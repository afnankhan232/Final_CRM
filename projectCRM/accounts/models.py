from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

# create a new user
# create a super user
class MyAccountManger(BaseUserManager):

    def create_user(self, company_email, company_name, password=None):

        if not company_email:
            raise ValueError("Users must have an Email!")
        if not company_name:
            raise ValueError("User must have a username!")

        user = self.model(
            company_email = self.normalize_email(company_email),
            company_name = company_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, company_email, company_name, password):
        user = self.create_user(
            company_email=self.normalize_email(company_email),
            company_name=company_name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True 
        user.is_superuser = True
        user.save(using=self._db)
        return user



def get_image_filepath(self, filename):
    return f'company_logos/{str(self.pk)}/{"logo.png"}'

def get_default_image():
    return f'company_logos/default/logo.png'

class BusinessUser(AbstractBaseUser):
    
    company_email = models.EmailField(max_length=60, unique=True)
    company_name = models.CharField(max_length=95, unique=True)

    industry = models.CharField(max_length=100, blank=True, null=True)

    job_title = models.CharField(max_length=255, blank=True, null=True)
    employees = models.IntegerField(default=None, blank=True, null=True)

    website = models.URLField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    country = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    last_login = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    company_logo = models.ImageField(upload_to=get_image_filepath, blank=True, null=True, default=get_default_image)

    objects = MyAccountManger()

    USERNAME_FIELD = 'company_email'
    REQUIRED_FIELDS = ['company_name']

    def __str__(self):
        return f"{self.company_email} - {self.company_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_logo_filename(self):
        return str(self.company_logo)[str(self.company_logo).index(f'company_logos/{self.pk}/'):]

# python manage.py migrate && python manage.py createsuperuser && python manage.py makemigrations && python manage.py migrate

