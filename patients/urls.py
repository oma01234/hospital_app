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
    path('patients/logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),

    path('message/<int:message_id>/', views.view_message, name='view_message'),
    path('medication-reminders/', views.medication_reminders, name='medication_reminders'),
    # path('bill-list/', views.bill_list, name='bill_list'),
    path('treatment-plans/', views.treatment_plans, name='treatment_plans'),  # New Treatment Plans URL
    path('emergency-contact/', views.emergency_contact, name='emergency_contact'),  # New Emergency Contact URL
    path('feedback/', views.feedback_form, name='feedback_form'),

    # Patient messages
    path('patient/messages/', views.patient_messages, name='patient_messages'),

    path('reports/', views.report_list, name='report_list'),
    path('report/<int:report_id>/', views.report_detail, name='report_detail'),
    path('report/download/<int:report_id>/', views.download_report, name='download_report'),

    # API views
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', LoginView.as_view(), name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),

    path('api/profile/', ProfileView.as_view(), name='api_profile'),
    path('api/profile/update/', UpdateProfileView.as_view(), name='api_update_profile'),

    # API endpoints for Medication & Treatment Reminders, Billing, Feedback
    path('api/medication-reminders/', MedicationReminderViewSet.as_view, name='api_medication_reminders'),
    path('api/treatment-plans/', TreatmentPlanViewSet.as_view, name='api_treatment_plans'),
    # path('api/bills/', BillViewSet.as_view, name='api_bills'),
    path('api/feedback/', FeedbackViewSet.as_view, name='api_feedback'),
    path('api/emergency/', EmergencyServiceViewSet.as_view, name='api_emergency_services'),
]
