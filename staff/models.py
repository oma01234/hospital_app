# models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from patients.models import Patient


class Staff(models.Model):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('admin', 'Administrator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff_profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    specialty = models.CharField(max_length=100, blank=True, null=True)  # Only for doctors
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def is_doctor(self):
        return self.role == 'doctor'


class DoctorSchedule(models.Model):
    def clean(self):
        # Ensure only doctors can have a schedule
        if self.doctor.role != 'doctor':
            raise ValidationError("Only staff members with the role 'Doctor' can have a schedule.")

        # Ensure start times are before end times
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            start_time = getattr(self, f"{day}_start")
            end_time = getattr(self, f"{day}_end")
            if start_time >= end_time:
                raise ValidationError(f"Invalid schedule: {day.capitalize()} start time must be before end time.")

    def __str__(self):
        return f"Schedule for {self.doctor.user.username}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='staff_appointment_patient')
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='appointments_assigned')
    scheduled_time = models.DateTimeField()
    reason = models.TextField(blank=True, null=True)  # Make reason optional
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'),
                                                      ('canceled', 'Canceled')], default='scheduled')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['patient', 'doctor', 'scheduled_time'], name='unique_appointment')
        ]
    
    def __str__(self):
        return f"Appointment for {self.patient.user.username} with Dr. {self.doctor.user.username}"

    def complete_appointment(self):
        self.status = 'completed'
        self.save()


# remove this form patients dashboard
class ConsultationNote(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='note')
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='consultation_notes')
    note = models.TextField()
    prescription = models.TextField(blank=True, null=True)
    treatment_plan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Consultation Note for {self.appointment.patient.username}"


class Assignment(models.Model):
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='doctor_assignments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Assignment of {self.patient.username} to Dr. {self.doctor.username}"


class VitalSign(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vitals')
    recorded_at = models.DateTimeField(auto_now_add=True)
    blood_pressure = models.CharField(max_length=20)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    pulse = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    oxygen_saturation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Vitals for {self.patient.username} recorded on {self.recorded_at}"

class ProgressTracking(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='progress')
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='progress_reports')
    recorded_at = models.DateTimeField(auto_now_add=True)
    progress_notes = models.TextField()

    def __str__(self):
        return f"Progress for {self.patient.username} by Dr. {self.doctor.username}"

class CarePlan(models.Model):
    patient = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='care_plans')
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='care_plans_created')
    plan_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Care Plan for {self.patient.username} by Dr. {self.doctor.username}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='staff_medical_records')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    diagnoses = models.TextField()
    treatment_history = models.TextField()
    allergies = models.TextField()
    family_history = models.TextField()
    medications = models.TextField()

    def __str__(self):
        return f"Medical Record for {self.patient.username}"

class LabTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_tests')
    test_name = models.CharField(max_length=255)
    test_date = models.DateTimeField(auto_now_add=True)
    ordered_by = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='ordered_tests')
    status = models.CharField(max_length=50, choices=[('ordered', 'Ordered'), ('completed', 'Completed')], default='ordered')

    def __str__(self):
        return f"{self.test_name} for {self.patient.username}"

class LabResult(models.Model):
    lab_test = models.OneToOneField(LabTest, on_delete=models.CASCADE, related_name='result')
    result_data = models.TextField()
    result_date = models.DateTimeField(auto_now_add=True)
    findings = models.TextField()

    def __str__(self):
        return f"Result for {self.lab_test.test_name} - {self.lab_test.patient.username}"


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='staff_prescriptions')
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='prescriptions_written')
    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    instructions = models.TextField()

    def __str__(self):
        return f"Prescription for {self.patient.username} by Dr. {self.doctor.username}"


class StaffMessage(models.Model):
    sender = models.ForeignKey(Staff, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Staff, related_name='received_messages', on_delete=models.CASCADE)
    message_content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username} at {self.sent_at}"


class DoctorPatientMessage(models.Model):
    sender = models.ForeignKey(Staff, related_name='sent_patient_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Patient, related_name='received_messages', on_delete=models.CASCADE)
    message_content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient} at {self.sent_at}"


class TeamMessage(models.Model):
    sender = models.ForeignKey(Staff, related_name='sent_team_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Profile, related_name='team_received_messages', on_delete=models.CASCADE)
    message_content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Team message from {self.sender.username} to {self.recipient} at {self.sent_at}"


class InsuranceProvider(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Insurance(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="insurance")
    insurance_provider = models.CharField(max_length=255)
    policy_number = models.CharField(max_length=255)
    coverage_start_date = models.DateField()
    coverage_end_date = models.DateField()
    coverage_details = models.TextField()

    def __str__(self):
        return f"Insurance for {self.profile.user.username}"


class Bill(models.Model):
    profile = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="bills")
    bill_number = models.CharField(max_length=255, unique=True)
    date_created = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('partially_paid', 'Partially Paid')])
    item_description = models.CharField(max_length=255, unique=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bill #{self.bill_number} for {self.profile.user.username}"


class InsuranceClaim(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="insurance_claims")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="insurance_claims")
    claim_number = models.CharField(max_length=255, unique=True)
    claim_date = models.DateField(auto_now_add=True)
    claim_status = models.CharField(max_length=50, choices=[('submitted', 'Submitted'), ('approved', 'Approved'), ('denied', 'Denied')])
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    reimbursement_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('partially_paid', 'Partially Paid')])
    date_submitted = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"Claim #{self.claim_number} for {self.profile.user.username}"


class EmergencyAlert(models.Model):
    ALERT_TYPES = [
        ('deterioration', 'Patient Deterioration'),
        ('critical_lab', 'Critical Lab Result'),
        ('other', 'Other'),
    ]

    profile = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='emergency_alerts')  # Linked to Profile
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    message = models.TextField()
    status = models.CharField(max_length=20, default='pending')  # pending, acknowledged, resolved
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Alert for {self.profile.user.username} - {self.alert_type}"


class MedicalSupply(models.Model):
    SUPPLY_TYPES = [
        ('medication', 'Medication'),
        ('equipment', 'Equipment'),
        ('consumable', 'Consumable'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    supply_type = models.CharField(max_length=50, choices=SUPPLY_TYPES)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)  # Threshold for reordering
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_below_reorder_level(self):
        return self.quantity_in_stock <= self.reorder_level


class StockAlert(models.Model):
    supply = models.ForeignKey(MedicalSupply, on_delete=models.CASCADE, related_name='alerts')
    alert_message = models.TextField()
    alert_status = models.CharField(max_length=20, default='unresolved')  # unresolved, resolved
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Alert for {self.supply.name} - {self.alert_message}"


class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True)
    supply = models.ForeignKey(MedicalSupply, on_delete=models.CASCADE, related_name='orders')
    quantity_ordered = models.PositiveIntegerField()
    order_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"Order #{self.order_number} for {self.supply.name}"


class HospitalPerformanceMetrics(models.Model):
    bed_occupancy = models.PositiveIntegerField(default=0)
    staff_available = models.PositiveIntegerField(default=0)
    patient_flow = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Metrics (Updated: {self.updated_at})"



class ResourceAllocation(models.Model):
    resource_type = models.CharField(max_length=50)  # e.g., 'Room', 'Equipment', 'Staff'
    resource_name = models.CharField(max_length=100)
    is_allocated = models.BooleanField(default=False)
    allocated_to = models.CharField(max_length=100, blank=True, null=True)
    allocation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resource_type} - {self.resource_name}"


class PerformanceAnalytics(models.Model):
    patient_satisfaction_score = models.FloatField()
    treatment_outcomes_score = models.FloatField()
    staff_performance_score = models.FloatField()
    report_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Analytics (Date: {self.report_date})"


class Report(models.Model):
    title = models.CharField(max_length=255)
    report_type = models.CharField(
        max_length=50,
        choices=[('patient_care', 'Patient Care'), ('financial', 'Financial'), ('performance', 'Performance')]
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='reports')
    file_path = models.FileField(upload_to='reports/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.report_type})"



class AuditLog(models.Model):
    user = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=255)
    model_name = models.CharField(max_length=100)
    model_instance_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} on {self.model_name} ({self.model_instance_id})"


class HealthAndSafetyProtocol(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class InfectionControlPractice(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_compliant = models.BooleanField(default=False)
    last_audited = models.DateTimeField()
    protocol = models.ForeignKey(HealthAndSafetyProtocol, related_name="infection_control_practices", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.protocol.name}"



class Certification(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    expiration_date = models.DateField()
    staff = models.ForeignKey(Staff, related_name='certifications', on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.staff.first_name} {self.staff.last_name})"


class Notification(models.Model):
    message = models.CharField(max_length=255)
    recipient = models.ForeignKey(Staff, on_delete=models.CASCADE)  # Link to user (patient or staff)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, choices=[('appointment', 'Appointment'), ('bill_payment', 'Bill Payment'), ('emergency', 'Emergency')])
    is_urgent = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.message}"
