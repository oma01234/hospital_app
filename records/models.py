from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# this is supposed to be updated by only staff yes?
class MedicalRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records_medical_records')
    diagnosis = models.TextField()
    treatment = models.TextField()
    date_recorded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Medical Record for {self.patient.username} on {self.date_recorded}"

class HealthReport(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_reports')
    report_name = models.CharField(max_length=100)
    report_file = models.FileField(upload_to='health_reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.report_name

class Prescription(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records_prescriptions')
    prescription_details = models.TextField()
    issued_at = models.DateField(auto_now_add=True)
    expires_at = models.DateField()

    def __str__(self):
        return f"Prescription for {self.patient.username} issued on {self.issued_at}"
