from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

RELATIONSHIP_CHOICES = [
    ('Parent', 'Parent'),
    ('Sibling', 'Sibling'),
    ('Spouse', 'Spouse'),
    ('Friend', 'Friend'),
]


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Patient')
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # Add any other fields that are specific to patients, such as medical history, etc.

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    insurance_details = models.TextField(blank=True, null=True)
    
    next_of_kin_name = models.CharField(max_length=100, blank=True, null=True)
    next_of_kin_phone_number = models.CharField(max_length=15, blank=True, null=True)
    next_of_kin_email = models.EmailField(blank=True, null=True)
    next_of_kin_address = models.TextField(blank=True, null=True)
    next_of_kin_relationship = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.user.username}"


class MedicationReminder(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medication_reminders')
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    time = models.TimeField()
    reminder_text = models.TextField()
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.medication_name} for {self.patient.user.username} at {self.time}"


class TreatmentPlan(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='treatment_plans')
    treatment_description = models.TextField()
    start_date = models.DateField()
    progress_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Treatment Plan for {self.patient.user.username}"

#
# class Bill(models.Model):
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='bills')
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     due_date = models.DateField()
#     is_paid = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"Bill for {self.patient.username} - {self.total_amount}"


class Feedback(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='feedback')
    rating = models.PositiveIntegerField(default=0)
    comments = models.TextField()

    def __str__(self):
        return f"Feedback from {self.patient.user.username} - Rating: {self.rating}"


class EmergencyService(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)  # Location or coordinates
    emergency_type = models.CharField(max_length=100)  # E.g., "Heart Attack", "Accident"
    request_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emergency Request for {self.patient.user.username} at {self.location}"


class TokenLog(models.Model):
    user = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_user')
    token = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Access token for {self.user.user.username}"

