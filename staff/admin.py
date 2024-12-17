from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here

# Register the custom admin for Staff

admin.site.register(Staff)  # Register the Staff model
admin.site.register(DoctorSchedule)
admin.site.register(Appointment)
admin.site.register(ConsultationNote)
admin.site.register(Assignment)
admin.site.register(VitalSign)
admin.site.register(ProgressTracking)
admin.site.register(CarePlan)
admin.site.register(MedicalRecord)
admin.site.register(LabTest)
admin.site.register(LabResult)
admin.site.register(Prescription)
admin.site.register(StaffMessage)
admin.site.register(DoctorPatientMessage)
admin.site.register(TeamMessage)
admin.site.register(Insurance)
admin.site.register(Bill)
admin.site.register(InsuranceClaim)
admin.site.register(EmergencyAlert)
admin.site.register(MedicalSupply)
admin.site.register(StockAlert)
admin.site.register(Order)
admin.site.register(HospitalPerformanceMetrics)
admin.site.register(ResourceAllocation)
admin.site.register(PerformanceAnalytics)
admin.site.register(Report)
admin.site.register(AuditLog)
admin.site.register(HealthAndSafetyProtocol)
admin.site.register(InfectionControlPractice)
admin.site.register(Certification)
admin.site.register(Notification)