from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Appointment

@receiver(post_save, sender=Appointment)
def send_appointment_reminder(sender, instance, created, **kwargs):
    if created:
        subject = "Appointment Confirmation"
        message = f"Dear {instance.patient.username}, your appointment with {instance.doctor} is confirmed for {instance.date} at {instance.time}."
        send_mail(subject, message, 'admin@hospitalapp.com', [instance.patient.email])
