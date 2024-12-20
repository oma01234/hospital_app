from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Medical Records
def medical_records(request):
    records = MedicalRecord.objects.filter(patient=request.user)
    return render(request, 'records/medical_records.html', {'records': records})

# Health Reports
def health_reports(request):
    reports = HealthReport.objects.filter(patient=request.user)
    return render(request, 'records/health_reports.html', {'reports': reports})

# Prescriptions
def prescriptions(request):
    prescriptions = Prescription.objects.filter(patient=request.user)
    return render(request, 'records/prescriptions.html', {'prescriptions': prescriptions})
