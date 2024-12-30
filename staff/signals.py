from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import AuditLog
from appointments.models import Appointment as AppointmentsAppointment
from staff.models import Appointment as StaffAppointment


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


@receiver(post_save, sender=StaffAppointment)
def create_or_update_appointment(sender, instance, **kwargs):
    # Synchronize data with the other model
    linked_appointment, created = AppointmentsAppointment.objects.update_or_create(
        linked_appointment=instance,
        defaults={
            'patient': instance.patient,
            'doctor': instance.doctor,
            'date': instance.scheduled_time.date(),
            'time': instance.scheduled_time.time(),
            'reason': instance.reason,
            'status': instance.status,
        }
    )
    instance.linked_appointment = linked_appointment
    instance.save()