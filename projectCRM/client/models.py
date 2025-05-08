# Basic
from django.db import models
from accounts.models import BusinessUser
from accounts.models import Role

# for Date Time field
from django.utils import timezone

# Validation Error
from django.core.exceptions import ValidationError

# Need to validate phone number
from django.core.validators import RegexValidator

# ---- ==== TRASH SOLUTION ==== ----
# Base Model to Implement Trash Solution to every Object!
class BaseModel(models.Model):
    is_deleted = models.BooleanField(default = False)
    deleted_at = models.DateTimeField(null = True, blank = True)

    class Meta:
        abstract = True
    
    # Temporary Delete (just change the filed value!)
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    # Restore deleted file
    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()
    
# CustomManager to add filter querySet
class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)


# Validator for country code: + followed by 1–4 digits
COUNTRY_CODE_CHOICES = [
    ('+1', 'United States (+1)'),
    ('+44', 'United Kingdom (+44)'),
    ('+91', 'India (+91)'),
    ('+81', 'Japan (+81)'),
    ('+61', 'Australia (+61)'),
    ('+49', 'Germany (+49)'),
    ('+971', 'UAE (+971)'),
    ('+86', 'China (+86)'),
    ('+33', 'France (+33)'),
]

# Validator for phone number: digits only, usually 7–12 digits depending on country
phone_number_validator = RegexValidator(
    regex=r'^\d{5,12}$',
    message="Enter a valid phone number without country code."
)

# ---- ==== Leads Model ==== ----
# INCLUDE [priority; status; name; email; description; created_at; created_by; modified_at; user; ]
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


# ---- ==== Project Model ==== ----
# Inherit: [is_deleted; deleted_at; ]
# Include: [name; description; user; ]
# Method: [objects; all_objects; ]
class Project(BaseModel):

    # Necessary Field [Project Name]
    name = models.CharField(max_length=255)

    # An Optional Description Field
    description = models.TextField(null = True, blank = True)

    # Linking with BusinessUser Model (every user have their own unique set of contacts that they can add and access)
    user = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)

    # Trash Implementation
    # Custom Manager hides the deleted Client {effect: Project.objects.filter()}
    objects = CustomManager()
    # Default Manager brings all the Client {effect: Project.all_objects.filter()}
    all_objects = models.Manager()

    # Adding META class - cause we need unique project name [inside each user]
    class Meta:
        unique_together = ('name', 'user', )

    # dunder str method, so we get better naming at the admin page [DEVELOPMENT SPECIFIC]
    def __str__(self):
        return f'{self.name}'

class ProjectAccessPermission(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="shared_project_permissions")
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    can_read_project = models.BooleanField(default = False)
    can_edit_project = models.BooleanField(default = False)
    can_delete_project = models.BooleanField(default = False)
    can_permanent_delete_project = models.BooleanField(default = False)
    # class Meta:
    #     unique_together = ('project', 'role')
    def __str__(self):
        return f"{self.role.user.company_email} [Role] {self.role.name} [can access] {self.project.name}"

# ---- ==== Client Model ==== ----
# Inherit: [is_deleted; deleted_at; ]
# Include: [name; email; country_code; phone; address; description; is_active; created_at; last_edit; list; companyAssignee; ]
# Method: [full_number; clean; objects; all_objects; ]
class Client(BaseModel):

    # Necessary Field
    name = models.CharField(max_length=255)

    # Email
    email = models.CharField(max_length=80)
    # Phone Number ['country_code' -> 'phone_number] + Exceptional
    country_code = models.CharField(
        max_length=5,
        choices=COUNTRY_CODE_CHOICES,
        default='+91',
        blank = True,
        null = True,
    )
    phone = models.CharField(
        max_length=12,
        validators=[phone_number_validator],
        blank = True,
        null = True,
    )

    # A method displaying full number
    def full_number(self):
        return f"{self.country_code}{self.phone_number}"

    # Over-riding clean method [to allow one of the field (email, phone_number) to be provided at the time of Client creation]
    def clean(self):
        super().clean()
        if not self.email and not self.phone:
            raise ValidationError('At least of the field ("email" or "phone_number") must be provided!')


    # Exceptional Field
    address = models.CharField(max_length=255, blank = True, null = True)

    # Exceptional Field
    description = models.TextField(blank = True, null = True)

    # A binary Field (Defaul set to 'True')
    is_active = models.BooleanField(default=True)

    # Field - [Created]
    created_at = models.DateTimeField(auto_now_add=True)

    # Field - [last edited]
    last_edit = models.DateTimeField(auto_now = True)

    # Trash Implementation
    # Custom Manager hides the deleted Client {effect: Project.objects.filter()}
    objects = CustomManager()
    # Default Manager brings all the Client {effect: Project.all_objects.filter()}
    all_objects = models.Manager()

    # Adding OneToOne field [linking with contact
    list = models.ForeignKey(Project, on_delete=models.CASCADE)

    # Linking with BusinessUser Model (every user have their own unique set of contacts that they can add and access)
    # models.CASCADE refers that if the BusinessUser is deleted, then delete the Client table from the database..
    companyAssignee = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)

    # dunder str method, so we get better naming at the admin page (DEVELOPMENT SPECIFIC)
    def __str__(self):
        return f'{self.name}'
    

# ---- ==== Document Model ==== ----
# Inherit: [is_deleted; deleted_at]
# Include: [document_name, file; related_to; uploaded_at; description; user; ]
# Method: [objects; all_objects; __str__; ]
class Document(BaseModel):

    # Adding Necessary Field
    document_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')

    # A Foreign Key Connected to [Client]
    related_to = models.ForeignKey(Client, on_delete=models.CASCADE)

    # Time when the field is added - just for analysis
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Exceptional Field
    description = models.TextField(blank = True, null = True)

    # Trash Implementation
    # Custom Manager hides the deleted Client {effect: Project.objects.filter()}
    objects = CustomManager()
    # Default Manager brings all the Client {effect: Project.all_objects.filter()}
    all_objects = models.Manager()

    # Linking with BusinessUser Model (every user have their own unique set of contacts that they can add and access)
    # models.CASCADE refers that if the BusinessUser is deleted, then delete the Client table from the database..
    user = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.document_name

class Task(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In-Progress', 'In-Progress'),
        ('Completed', 'Completed'),
    ]
    PRIORITY_CHOICES = [
        ('Normal', 'Normal'),
        ('Urgent', 'Urgent'),
        ('Low', 'Low'),
    ]
    TYPE_CHOICES = [
        ('Call', 'Call'),
        ('WhatsApp', 'WhatsApp'),
        ('Gmail', 'Gmail'),
        ('Other', 'Other'),
    ]

    task_name = models.CharField(max_length=255)
    description = models.TextField(null = True, blank = True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Normal')
    owner = models.ForeignKey(BusinessUser, related_name='owned_tasks' ,on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    related_to = models.ForeignKey(Client, on_delete=models.CASCADE)
    due_date = models.DateField()
    due_time = models.TimeField()

    user = models.ForeignKey(BusinessUser, related_name='assigned_tasks', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.task_name} ({self.status})'

# This should be deleted!
class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)