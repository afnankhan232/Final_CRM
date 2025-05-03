from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from .models import BusinessUser

@receiver(post_save, sender=User)
def create_business_user(sender, instance, created, **kwargs):
    if created:
        # Try to fetch Google account data if it's a social login
        try:
            social_account = SocialAccount.objects.get(user=instance, provider='google')
            extra_data = social_account.extra_data
            name = extra_data.get('name', instance.username)
            email = extra_data.get('email', instance.email)
        except SocialAccount.DoesNotExist:
            # fallback for non-social login
            name = instance.username
            email = instance.email

        BusinessUser.objects.create(
            user=instance,
            company_name=name,
            company_email=email
        )

@receiver(post_save, sender=User)
def save_business_user(sender, instance, **kwargs):
    # Only save if BusinessUser already exists
    if hasattr(instance, 'businessuser'):
        instance.businessuser.save()