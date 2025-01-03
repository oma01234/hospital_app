# views.py (API views)
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializer import *
from .permissions import IsDoctor, IsAdmin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .utils import generate_report_pdf
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from patients.models import Patient
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


# Define the permission classes
class StaffPermission(IsAuthenticated):
    def has_permission(self, request, view):
        return hasattr(request.user, 'staff')


# adjust the apis to work properly, especially the staff p
class DoctorPermission(IsDoctor):
    def has_permission(self, request, view):
        # Ensure user is a doctor by checking role
        return hasattr(request.user, 'staff') and request.user.staff.role == 'doctor'


# Staff viewset to manage staff through the API
class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [AllowAny]  # Only staff can access this

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Send a POST request with user registration details."}, status=status.HTTP_200_OK)

    def post(self, request):
        print('data sent')
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            staff = serializer.save()
            return Response({'message': 'Registration successful!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Doctor viewset (access restricted to doctors)
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.filter(role='doctor')
    serializer_class = StaffSerializer
    permission_classes = [DoctorPermission]  # Only doctors can access this


class DoctorScheduleViewSet(viewsets.ModelViewSet):
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class VitalSignViewSet(viewsets.ModelViewSet):
    queryset = VitalSign.objects.all()
    serializer_class = VitalSign


class CarePlanViewSet(viewsets.ModelViewSet):
    queryset = CarePlan.objects.all()
    serializer_class = CarePlanSerializer


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer


class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer


class StaffMessageList(APIView):
    def get(self, request):
        messages = StaffMessage.objects.all()
        serializer = StaffMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StaffMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Send a message (POST request with sender and recipient data)
class SendStaffMessage(APIView):
    def post(self, request):
        serializer = StaffMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorPatientMessageList(APIView):
    def get(self, request, patient_id):
        # Ensure the patient exists before proceeding
        if not User.objects.filter(id=patient_id).exists():
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        messages = DoctorPatientMessage.objects.filter(patient_id=patient_id)
        serializer = DoctorPatientMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, patient_id):
        # Ensure the patient exists before creating the message
        if not User.objects.filter(id=patient_id).exists():
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = DoctorPatientMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient_id=patient_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamMessageList(APIView):
    def get(self, request, patient_id):
        messages = TeamMessage.objects.filter(patient_id=patient_id)
        serializer = TeamMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, patient_id):
        serializer = TeamMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient_id=patient_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InsuranceViewSet(viewsets.ModelViewSet):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


class InsuranceClaimViewSet(viewsets.ModelViewSet):
    queryset = InsuranceClaim.objects.all()
    serializer_class = InsuranceClaimSerializer


class EmergencyAlertCreateView(APIView):
    def post(self, request, format=None):
        serializer = EmergencyAlertSerializer(data=request.data)
        if serializer.is_valid():
            alert = serializer.save()
            return Response(EmergencyAlertSerializer(alert).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmergencyAlertListView(ListAPIView):
    queryset = EmergencyAlert.objects.all()
    serializer_class = EmergencyAlertSerializer


class EmergencyAlertUpdateView(APIView):
    def patch(self, request, pk, format=None):
        alert = EmergencyAlert.objects.get(pk=pk)
        serializer = EmergencyAlertSerializer(alert, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicalSupplyViewSet(viewsets.ModelViewSet):
    queryset = MedicalSupply.objects.all()
    serializer_class = MedicalSupplySerializer


class StockAlertViewSet(viewsets.ModelViewSet):
    queryset = StockAlert.objects.filter(alert_status='unresolved')
    serializer_class = StockAlertSerializer

    def perform_create(self, serializer):
        supply = serializer.validated_data['supply']
        if supply.is_below_reorder_level():
            alert_message = f"Stock for {supply.name} is below the reorder level."
            serializer.save(alert_message=alert_message)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class HospitalPerformanceMetricsViewSet(viewsets.ModelViewSet):
    queryset = HospitalPerformanceMetrics.objects.all()
    serializer_class = HospitalPerformanceMetricsSerializer


class ResourceAllocationViewSet(viewsets.ModelViewSet):
    queryset = ResourceAllocation.objects.all()
    serializer_class = ResourceAllocationSerializer


class PerformanceAnalyticsViewSet(viewsets.ModelViewSet):
    queryset = PerformanceAnalytics.objects.all()
    serializer_class = PerformanceAnalyticsSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        report = serializer.save(generated_by=self.request.user)
        file_path = generate_report_pdf(report)  # Utility function to generate PDF
        report.file_path = file_path
        report.save()


class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    http_method_names = ['get']



class HealthAndSafetyProtocolViewSet(viewsets.ModelViewSet):
    queryset = HealthAndSafetyProtocol.objects.all()
    serializer_class = HealthAndSafetyProtocolSerializer


class InfectionControlPracticeViewSet(viewsets.ModelViewSet):
    queryset = InfectionControlPractice.objects.all()
    serializer_class = InfectionControlPracticeSerializer


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)  # Get notifications for the logged-in user


# ViewSet for handling patients
class PatientViewSet(viewsets.ViewSet):

    # Search patients by username or email
    @action(detail=False, methods=['get'])
    def search_patient(self, request):
        query = request.query_params.get('q', '')
        if query:
            patients = Patient.objects.filter(user__username__icontains=query) | Patient.objects.filter(
                user__email__icontains=query)
        else:
            patients = Patient.objects.all()

        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    # Display details of a specific patient
    @action(detail=True, methods=['get'])
    def display_patient(self, request, pk=None):
        try:
            patient = Patient.objects.get(id=pk)
        except Patient.DoesNotExist:
            raise NotFound("Patient not found")

        serializer = PatientSerializer(patient)
        return Response(serializer.data)
