from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import AuditLog
from django.db import IntegrityError
from appointments.models import Appointment as AppointmentsAppointment
from staff.models import Appointment as StaffAppointment


@receiver(post_save)
def create_audit_log(sender, instance, created, **kwargs):
    # Replace 'your_app_name' with the actual app label of your models
    if sender._meta.app_label == 'staff' and sender.__name__ != 'AuditLog':  # Exclude AuditLog
        created_by = getattr(instance, 'created_by', None)
        instance_id = getattr(instance, 'id', None)
        if instance_id is None:
            return

        # Prevent recursive signal calls
        if not getattr(instance, '_disable_audit_log', False):
            try:
                instance._disable_audit_log = True
                AuditLog.objects.create(
                    user=created_by,
                    action='Created' if created else 'Updated',
                    model_name=sender.__name__,
                    model_instance_id=instance_id
                )
            finally:
                instance._disable_audit_log = False



@receiver(pre_delete)
def delete_audit_log(sender, instance, **kwargs):
    # Filter for only specific app models if applicable
    if sender._meta.app_label == 'staff':
        created_by = getattr(instance, 'created_by', None)
        instance_id = getattr(instance, 'id', None)

        if instance_id is not None:
            AuditLog.objects.create(
                user=created_by,
                action='Deleted',
                model_name=sender.__name__,
                model_instance_id=instance_id
            )



@receiver(post_save, sender=StaffAppointment)
def create_patient_appointment(sender, instance, created, **kwargs):
    if created and not instance.linked_appointment:
        # Check if an appointment already exists with the same patient, doctor, and scheduled time
        existing_appointment = AppointmentsAppointment.objects.filter(
            patient=instance.patient,
            doctor=instance.doctor,
            date=instance.scheduled_time.date(),
            time=instance.scheduled_time.time()
        ).exists()

        if existing_appointment:
            print('Appointment already exists for this patient, doctor, and time.')
            return  # Exit early if the appointment already exists

        # Create the corresponding appointment in the other app if no existing appointment is found
        try:
            linked_appointment = AppointmentsAppointment.objects.create(
                patient=instance.patient,
                doctor=instance.doctor,
                date=instance.scheduled_time.date(),
                time=instance.scheduled_time.time(),
                reason=instance.reason,
                is_confirmed=True if instance.status == 'scheduled' else False,
                consultation_type='Physical'  # Adjust based on your requirements
            )
            if linked_appointment:
                print('created_for_2')
            else:
                print('nope')

            # Link the two appointments
            instance.linked_appointment = linked_appointment
            instance.save()

        except IntegrityError:
            print('IntegrityError occurred when trying to create the appointment.')



@receiver(post_delete, sender=StaffAppointment)
def delete_linked_appointment(sender, instance, **kwargs):
    if instance.linked_appointment:
        instance.linked_appointment.delete()
