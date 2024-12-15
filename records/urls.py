from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import medical_records, health_reports, prescriptions
from .api_views import MedicalRecordViewSet, HealthReportViewSet, PrescriptionViewSet

app_name = 'records'

# Create a router for API endpoints
router = DefaultRouter()
router.register(r'medical-records', MedicalRecordViewSet, basename='medical_record')
router.register(r'health-reports', HealthReportViewSet, basename='health_report')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')

urlpatterns = [
    # Template-based views
    path('medical-records/', medical_records, name='medical_records'),
    path('health-reports/', health_reports, name='health_reports'),
    path('prescriptions/', prescriptions, name='prescriptions'),

    # API endpoints
    path('api/', include(router.urls)),
]
