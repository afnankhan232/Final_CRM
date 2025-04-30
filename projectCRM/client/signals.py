from django.db.models.signals import post_save
from django.dispatch import receiver

# Authentication USER
from accounts.models import BusinessUser

# MODEL to which we wanna create the signal for (as the default value).
from .models import Project

# Creating signal [for] creating a default project value (default) which will contain data of every project!
@receiver(post_save, sender=BusinessUser)
def create_default_project(sender, instance, created, **kwargs):
    if created:
        Project.objects.create(name = "Default", user = instance)