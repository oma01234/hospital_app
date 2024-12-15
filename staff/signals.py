from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import AuditLog

@receiver(post_save)
def create_audit_log(sender, instance, created, **kwargs):
    if not sender._meta.label_lower.startswith('auth.'):  # Ignore auth-related models
        AuditLog.objects.create(
            user=instance.modified_by,  # Ensure your models track who modified them
            action='Created' if created else 'Updated',
            model_name=sender.__name__,
            model_instance_id=instance.id
        )

@receiver(pre_delete)
def delete_audit_log(sender, instance, **kwargs):
    if not sender._meta.label_lower.startswith('auth.'):
        AuditLog.objects.create(
            user=instance.modified_by,
            action='Deleted',
            model_name=sender.__name__,
            model_instance_id=instance.id
        )
