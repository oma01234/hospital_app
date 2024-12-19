from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


# adjust this so it's just the patients that has this model, think of another profile to associate staff with
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    insurance_details = models.TextField(blank=True, null=True)
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='modified_profiles')
    next_of_kin = ''
    next_of_kin_details = 'blah, blah, blah'


    def __str__(self):
        return f"Profile for {self.user.username}"

class MedicationReminder(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medication_reminders')
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    time = models.TimeField()
    reminder_text = models.TextField()
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.medication_name} for {self.patient.username} at {self.time}"

class TreatmentPlan(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='treatment_plans')
    treatment_description = models.TextField()
    start_date = models.DateField()
    progress_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Treatment Plan for {self.patient.username}"

class Bill(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bills')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Bill for {self.patient.username} - {self.total_amount}"

class Feedback(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
    rating = models.PositiveIntegerField(default=0)
    comments = models.TextField()

    def __str__(self):
        return f"Feedback from {self.patient.username} - Rating: {self.rating}"


class EmergencyService(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)  # Location or coordinates
    emergency_type = models.CharField(max_length=100)  # E.g., "Heart Attack", "Accident"
    request_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emergency Request for {self.patient.username} at {self.location}"
