from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings

# set this guy to populate the list of staff with role = doctor
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.specialization}"

class Appointment(models.Model):
    CONSULTATION_TYPE_CHOICES = [
        ('Physical', 'Physical'),
        ('Virtual', 'Virtual'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_patient')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    is_confirmed = models.BooleanField(default=False)
    consultation_type = models.CharField(max_length=50, choices=CONSULTATION_TYPE_CHOICES, default='Physical')

    def __str__(self):
        return f"{self.patient.username} with {self.doctor.user.username} on {self.date} at {self.time}"

class ConsultationNote(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='consultation_note')
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notes for {self.appointment.patient.username} - {self.appointment.consultation_type}"
