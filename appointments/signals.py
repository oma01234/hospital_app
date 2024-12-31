from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Appointment as PatientAppointment
from staff.models import Appointment
from datetime import datetime

@receiver(post_save, sender=PatientAppointment)
def send_appointment_reminder(sender, instance, created, **kwargs):
    if created:
        subject = "Appointment Confirmation"
        message = f"Dear {instance.patient.user.username}, your appointment with {instance.doctor} is confirmed for {instance.date} at {instance.time}."
        # send_mail(subject, message, 'admin@hospitalapp.com', [instance.patient.email]) fix this one later


@receiver(post_save, sender=PatientAppointment)
def create_staff_appointment(sender, instance, created, **kwargs):
    if created:
        # Check if a linked appointment already exists
        if not hasattr(instance, 'staff_appointment'):
            # Create the corresponding appointment in the staff app
            linked_appointment = Appointment.objects.create(
                patient=instance.patient,
                doctor=instance.doctor,
                scheduled_time=datetime.combine(instance.date, instance.time),
                reason=instance.reason,
                status='scheduled' if instance.is_confirmed else 'pending'
            )
            if linked_appointment:
                print('created_for_1')
            else:
                print('nope')
            # Link the two appointments
            instance.staff_appointment = linked_appointment
            instance.save()
