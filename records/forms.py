from django import forms
from .models import MedicalRecord, HealthReport, Prescription

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'treatment']

class HealthReportForm(forms.ModelForm):
    class Meta:
        model = HealthReport
        fields = ['report_name', 'report_file']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['prescription_details', 'expires_at']
