from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=Patient)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Check if the User has a related Patient instance
        if hasattr(instance, 'Patient'):
            Profile.objects.create(user=instance)


@receiver(post_save, sender=Patient)
def save_profile(sender, instance, **kwargs):
    # Save profile only if the user has a related Patient instance
    if hasattr(instance, 'Patient'):
        instance.profile.save()