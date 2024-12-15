from rest_framework import viewsets, permissions
from .models import MedicalRecord, HealthReport, Prescription
from .serializers import MedicalRecordSerializer, HealthReportSerializer, PrescriptionSerializer

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(patient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class HealthReportViewSet(viewsets.ModelViewSet):
    queryset = HealthReport.objects.all()
    serializer_class = HealthReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(patient=self.request.user)

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(patient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)
