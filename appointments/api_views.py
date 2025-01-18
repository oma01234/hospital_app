from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import timezone


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(patient=self.request.user.Patient)
        consultation_type = self.request.query_params.get('consultation_type')
        if consultation_type:
            queryset = queryset.filter(consultation_type=consultation_type)
        return queryset

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.Patient)

    @action(detail=False, methods=['get'], url_path='consultation-history')
    def consultation_history(self, request):
        """
        Custom action to retrieve past and upcoming consultations for the authenticated patient.
        """
        now = timezone.now()
        patient = request.user.Patient

        past_appointments = Appointment.objects.filter(patient=patient, date__lt=now.date())
        upcoming_appointments = Appointment.objects.filter(patient=patient, date__gte=now.date())

        past_serializer = self.get_serializer(past_appointments, many=True)
        upcoming_serializer = self.get_serializer(upcoming_appointments, many=True)

        return Response({
            'past_appointments': past_serializer.data,
            'upcoming_appointments': upcoming_serializer.data
        })



class ConsultationNoteViewSet(viewsets.ModelViewSet):
    queryset = ConsultationNote.objects.all()
    serializer_class = ConsultationNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(appointment__patient=self.request.user.Patient)


class ConsultationHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = datetime.now().date()
        past_appointments = Appointment.objects.filter(patient=request.user.Patient, date__lt=today)
        upcoming_appointments = Appointment.objects.filter(patient=request.user.Patient, date__gte=today)

        return Response({
            "past_appointments": AppointmentSerializer(past_appointments, many=True).data,
            "upcoming_appointments": AppointmentSerializer(upcoming_appointments, many=True).data,
        })
