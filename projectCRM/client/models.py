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

class Project(models.Model):

    # Necessary Field [Project Name]
    name = models.CharField(max_length=255)

    # An Optional Description Field
    description = models.TextField(null = True, blank = True)

    # Linking with BusinessUser Model (every user have their own unique set of contacts that they can add and access)
    user = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)

    # Adding META class - cause we need unique project name [inside each user]
    class Meta:
        unique_together = ('name', 'user', )

    # dunder str method, so we get better naming at the admin page (DEVELOPMENT SPECIFIC)
    def __str__(self):
        return f'{self.name} - {self.user.company_name}'

class Client(models.Model):

    # Necessary Field
    name = models.CharField(max_length=255)

    # Email
    email = models.CharField(max_length=80)
    # Phone Number ['country_code' -> 'phone_number] + Exceptional
    country_code = models.IntegerField(default=91, blank = True, null = True)
    phone = models.IntegerField(blank = True, null = True)

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

    # Adding OneToOne field [linking with contact
    list = models.ForeignKey(Project, on_delete=models.CASCADE)

    # Linking with BusinessUser Model (every user have their own unique set of contacts that they can add and access)
    # models.CASCADE refers that if the BusinessUser is deleted, then delete the Client table from the database..
    companyAssignee = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)

    # dunder str method, so we get better naming at the admin page (DEVELOPMENT SPECIFIC)
    def __str__(self):
        return f'{self.name} - {self.companyAssignee.company_name}'
    


class Document(models.Model):

    # Adding Necessary Field
    document_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')

    # A Foreign Key Connected to [Client]
    related_to = models.ForeignKey(Client, on_delete=models.CASCADE)

    # Time when the field is added - just for analysis
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Exceptional Field
    description = models.TextField(blank = True, null = True)

    # Linking with BusinessUser Model (every user have their own unique set of contacts that they can add and access)
    # models.CASCADE refers that if the BusinessUser is deleted, then delete the Client table from the database..
    user = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.document_name



class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(BusinessUser, on_delete=models.CASCADE)