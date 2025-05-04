from django.db import models
from django.contrib.auth.models import User
import uuid

def get_image_filepath(self, filename):
    return f'company_logos/{str(self.pk)}/{"logo.png"}'

def get_default_image():
    return f'company_logos/default/logo.png'

class BusinessUser(models.Model):

    public_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
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

# ==== ---- Creation Role ---- ====
# INCLUDE: [name; can_read_contact; can_edit_contact; can_delete_contact; can_permanent_delete_contact; ...]
# INHERIT: [None; ]
# METHOD: [__str__; ]
class Role(models.Model):

    name = models.CharField(max_length = 50)

    can_read_contact = models.BooleanField(default = False)
    can_add_contact = models.BooleanField(default = False)
    can_edit_contact = models.BooleanField(default = False)
    can_delete_contact = models.BooleanField(default = False)
    can_permanent_delete_contact = models.BooleanField(default = False)

    can_add_project = models.BooleanField(default = False)

    can_read_tasks = models.BooleanField(default = False)
    can_add_tasks = models.BooleanField(default = False)
    can_edit_tasks = models.BooleanField(default = False)
    can_delete_tasks = models.BooleanField(default = False)
    can_permanent_delete_tasks = models.BooleanField(default = False)

    can_read_documents = models.BooleanField(default = False)
    can_add_documents = models.BooleanField(default = False)
    can_edit_documents = models.BooleanField(default = False)
    can_delete_documents = models.BooleanField(default = False)
    can_permanent_delete_documents = models.BooleanField(default = False)

    user = models.ForeignKey(
        BusinessUser,
        on_delete = models.CASCADE,
    )

    class Meta:
        unique_together = ('user', 'name', )

    def __str__(self):
        return self.user.company_email + " -> " + self.name


# ==== ---- Creating AccessPermission Model ---- ====
# INCLUDE: [owner: BusinessUser; shared_with: BusinessUser; role: Role; date_shared: DateTimeField; ]
# INHERIT: [None; ]
# METHOD: [unique_together; __str__; ]
class AccessPermission(models.Model):
    owner = models.ForeignKey(
        BusinessUser, 
        related_name = 'shared_with', 
        on_delete = models.CASCADE,
    )

    shared_with = models.ForeignKey(
        BusinessUser, 
        related_name='accessible_accounts',
        on_delete = models.CASCADE,
    )

    role = models.ForeignKey(
        Role, 
        on_delete = models.CASCADE,
    )

    date_shared = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ('owner', 'shared_with', )

    def __str__(self):
        return self.owner.company_email + " -> " + self.shared_with.company_email