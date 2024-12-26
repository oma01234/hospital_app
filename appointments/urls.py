from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .api_views import *

app_name = 'appointments'

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment'),
router.register(r'consultation-notes', ConsultationNoteViewSet, basename='consultation_note')

urlpatterns = [
    # Template-based views
    path('book/', book_appointment, name='book_appointment'),
    path('list/', appointment_list, name='appointment_list'),
    path('history/', consultation_history, name='consultation_history'),
    path('book-virtual/', book_virtual_consultation, name='book_virtual_consultation'),
    path('add-note/<int:appointment_id>/', add_consultation_note, name='add_consultation_note'),

    # API endpoints
    path('api/', include(router.urls)),

]
