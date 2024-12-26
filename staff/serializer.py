# serializers.py
from rest_framework import serializers
from .models import *
from patients.models import Patient

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'username', 'role', 'specialty', 'phone_number', 'profile_picture']


class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = [
            'id', 'doctor', 'monday_start', 'monday_end',
            'tuesday_start', 'tuesday_end', 'wednesday_start', 'wednesday_end',
            'thursday_start', 'thursday_end', 'friday_start', 'friday_end',
            'saturday_start', 'saturday_end', 'sunday_start', 'sunday_end'
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'scheduled_time', 'reason', 'status']


# serializers.py
class VitalSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSign
        fields = ['id', 'patient', 'recorded_at', 'blood_pressure', 'temperature', 'pulse', 'weight', 'oxygen_saturation']


class CarePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarePlan
        fields = ['id', 'patient', 'created_by', 'diagnosis', 'treatment_plan', 'follow_up_date']


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'record_type', 'details', 'date_created']

class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ['id', 'patient', 'test_name', 'result', 'date_conducted']


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'medication_name', 'dosage', 'instructions', 'end_date']


class StaffMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMessage
        fields = ['id', 'sender', 'recipient', 'message_content', 'sent_at']


class DoctorPatientMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorPatientMessage
        fields = ['id', 'sender', 'recipient', 'message_content', 'sent_at']


class TeamMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMessage
        fields = ['id', 'sender', 'recipient', 'message_content', 'sent_at']


class InsuranceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceProvider
        fields = '__all__'

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'

class InsuranceClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        fields = '__all__'


class EmergencyAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyAlert
        fields = ['id', 'profile', 'alert_type', 'message', 'status', 'created_at', 'updated_at', 'resolved_at']


class MedicalSupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalSupply
        fields = '__all__'


class StockAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockAlert
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class HospitalPerformanceMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalPerformanceMetrics
        fields = '__all__'

class ResourceAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceAllocation
        fields = '__all__'

class PerformanceAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceAnalytics
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'



class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'


class HealthAndSafetyProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthAndSafetyProtocol
        fields = '__all__'


class InfectionControlPracticeSerializer(serializers.ModelSerializer):
    protocol = HealthAndSafetyProtocolSerializer()

    class Meta:
        model = InfectionControlPractice
        fields = '__all__'



class CertificationSerializer(serializers.ModelSerializer):
    staff = StaffSerializer()

    class Meta:
        model = Certification
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'recipient', 'created_at', 'read', 'notification_type', 'is_urgent']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'  # Or specify the fields you need
