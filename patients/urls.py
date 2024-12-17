from django.urls import path
from . import views
from .api_views import *
from .views import *

app_name = 'patients'

urlpatterns = [

    path('', landing, name='landing'),

    # Template-based views
    path('patients/register/', views.register, name='register'),
    path('patients/login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),

    path('medication-reminders/', views.medication_reminders, name='medication_reminders'),
    path('bill-list/', views.bill_list, name='bill_list'),
    path('treatment-plans/', views.treatment_plans, name='treatment_plans'),  # New Treatment Plans URL
    path('emergency-contact/', views.emergency_contact, name='emergency_contact'),  # New Emergency Contact URL
    path('feedback/', views.feedback_form, name='feedback_form'),

    # API views
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/profile/', ProfileView.as_view(), name='api_profile'),

    # API endpoints for Medication & Treatment Reminders, Billing, Feedback
    path('api/medication-reminders/', MedicationReminderViewSet.as_view, name='api_medication_reminders'),
    path('api/treatment-plans/', TreatmentPlanViewSet.as_view, name='api_treatment_plans'),
    path('api/bills/', BillViewSet.as_view, name='api_bills'),
    path('api/feedback/', FeedbackViewSet.as_view, name='api_feedback'),
    path('api/emergency/', EmergencyServiceViewSet.as_view, name='api_emergency_services'),
]
