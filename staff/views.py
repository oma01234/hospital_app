# views.py
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.forms import *
from django.contrib.auth import login, authenticate
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.utils import timezone
from .forms import *
from django.http import FileResponse
from django.contrib.auth import logout
from django.contrib import messages
from patients.models import Profile
from urllib.parse import urlencode
from django.utils.timezone import now
from datetime import timedelta, datetime
from staff.models import Appointment as APP
from django.core.exceptions import ValidationError


def register(request):
    if request.method == 'POST':
        form = StaffUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save()  # Save the Staff user
            print('Staff user created successfully.')
            return redirect('staff:login')  # Redirect to the login page or another view
        else:
            print('Form is invalid.')
            print(form.errors)
    else:
        form = StaffUserCreationForm()

    return render(request, 'staff/register.html', {'form': form})


# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in
            return redirect('staff:dashboard')  # Redirect to the dashboard after login
        else:
            print('Form is invalid.')  # For debugging
            print(form.errors)  # Display form errors (consider showing this to the user)
            print("POST Data:", request.POST)
    else:
        form = AuthenticationForm()

    return render(request, 'staff/login.html', {'form': form})


def logout_view(request):
    alert_message = None

    if request.user.is_authenticated:
        try:
            # Get the user's Staff profile
            staff_profile = Staff.objects.get(user=request.user)

            # Determine the alert message based on the role
            if staff_profile.role == 'doctor':
                alert_message = "You are logging out as a doctor."
            elif staff_profile.role == 'nurse':
                alert_message = "You are logging out as a nurse."
            elif staff_profile.role == 'admin':
                alert_message = "You are logging out as an administrator."

        except Staff.DoesNotExist:
            # Handle the case where no Staff profile exists for the user
            alert_message = "No staff profile found for this user."

        # Log out the user
        logout(request)

    # Redirect to the login page with the alert message
    url = reverse('staff:login')  # Get the URL for the login page
    query_params = urlencode({'alert_message': alert_message})  # Encode the query parameters
    return redirect(f"{url}?{query_params}")
    # fix this guy later abeg

# Example view: Staff dashboard
@login_required
def staff_dashboard(request):
    # Check the user's role
    if request.user.staff_profile.role == 'doctor':
        return render(request, 'staff/doctor_dashboard.html')
    elif request.user.staff_profile.role == 'nurse':
        return render(request, 'staff/nurse_dashboard.html')
    elif request.user.staff_profile.role == 'admin':
        return render(request, 'staff/admin_dashboard.html')
    else:
        return HttpResponseForbidden("You don't have permission to view this page.")


def is_doctor(user):
    return user.staff.role == 'doctor'


@user_passes_test(is_doctor)
def doctor_view(request):
    # Doctor-specific view logic
    return render(request, 'staff/doctor_page.html')


@login_required
def doctor_schedule(request):
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    capitalized_days = [day.capitalize() for day in days]

    # Ensure the user is a doctor
    if not hasattr(request.user, 'staff_profile') or request.user.staff_profile.role != 'doctor':
        return redirect('staff:unauthorized')  # Or return an appropriate HTTP 403 response

    # Get or create the doctor's schedule
    doctor = request.user.staff_profile
    schedule, created = DoctorSchedule.objects.get_or_create(id=request.user.id, doctor=doctor)
    schedule_data = {day: {'start': getattr(schedule, f'{day}_start'), 'end': getattr(schedule, f'{day}_end')} for day
                     in days}

    if request.method == 'POST':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for day in days:
            start_time = request.POST.get(f'{day}_start')
            end_time = request.POST.get(f'{day}_end')

            # Validate and assign the times
            if start_time and end_time:
                if start_time >= end_time:
                    messages.error(request, f"{day.capitalize()} start time must be earlier than end time.")
                    return render(request, 'staff/doctor_schedule.html', {'schedule': schedule})

                # Set the attributes dynamically
                setattr(schedule, f'{day}_start', start_time)
                setattr(schedule, f'{day}_end', end_time)
            elif start_time or end_time:
                messages.error(request, f"Both start and end times must be filled for {day.capitalize()}.")
                return render(request, 'staff/doctor_schedule.html', {'schedule': schedule})

        # Save the schedule if validation passes
        try:
            schedule.full_clean()  # Validate the model
            schedule.save()
            messages.success(request, "Schedule updated successfully!")
        except ValidationError as e:
            messages.error(request, f"Validation error: {e.message_dict}")
        return redirect('staff:doctor_schedule')

    return render(request, 'staff/doctor_schedule.html', {'schedule': schedule, 'days':capitalized_days, 'schedule_data': schedule_data})


def unauthorized(request):
    return render(request, 'staff/unauthorized.html', status=403)


@login_required
def assign_appointment(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    available_doctors = Staff.objects.filter(role='doctor')

    if request.method == 'POST':
        reason = request.POST.get('reason')
        date_time = datetime.strptime(request.POST.get('date_time'), '%Y-%m-%dT%H:%M')
        day_of_week = date_time.strftime('%A').lower()  # Get the day of the week (e.g., 'monday')

        # Check if there are available doctors
        available_doctors = Staff.objects.filter(role='doctor')
        if not available_doctors.exists():
            messages.error(request, "No doctors available.")
            return redirect('staff:assign_appointment', patient_id=patient.id)

        for doctor in available_doctors:
            if doctor.doctor_schedule:
                schedule = doctor.doctor_schedule
                start_time = getattr(schedule, f"{day_of_week}_start", None)
                end_time = getattr(schedule, f"{day_of_week}_end", None)

                if start_time and end_time and start_time <= date_time.time() <= end_time:
                    # Check for conflicting appointments
                    conflicting_appointments = Appointment.objects.filter(
                        doctor=doctor,
                        scheduled_time__gte=date_time,
                        scheduled_time__lt=date_time + timedelta(minutes=30)
                    )
                    if not conflicting_appointments.exists():
                        # Create the appointment and include created_by
                        created_by = request.user.staff_profile  # Assuming the logged-in user has a staff profile
                        appointment = Appointment.objects.create(
                            patient=patient,
                            doctor=doctor,
                            created_by=created_by,
                            scheduled_time=date_time,
                            reason=reason,
                            status='scheduled'
                        )
                        print('created_for_3')
                        messages.success(request, f"Appointment scheduled with Dr. {doctor.user.get_full_name()}")
                        return redirect('staff:display_patient', patient_id=patient.id)

            else:
                # Handle the case where the doctor doesn't have a schedule
                # (e.g., display a message or skip this doctor in the loop)
                pass

        messages.error(request, "No doctors are available at the selected time.")
        return redirect('staff:assign_appointment', patient_id=patient.id)

    return render(request, 'staff/assign_appointment.html', {'patient': patient, 'doctors': available_doctors})


@login_required
def view_appointment(request, appointment_id):
    # Get the appointment and ensure it's not cancelled
    appointment = get_object_or_404(Appointment, id=appointment_id, status__ne='Cancelled')

    # Check if the logged-in user is the doctor for the appointment
    if appointment.doctor != request.user.Staff:
        return redirect('unauthorized')

    # Fetch the consultation note if it exists
    note = ConsultationNote.objects.filter(appointment=appointment).first()

    return render(request, 'staff/view_appointment.html', {'appointment': appointment, 'note': note})


def view_patient_appointments(request, patient_i):
    # Fetch the patient object
    patient = get_object_or_404(Patient, id=patient_i)

    # Fetch all appointments for the patient
    appointments = APP.objects.filter(patient_id=patient_i)
    # for app in appointments:
    #     date = app.scheduled_time.date()  # Corrected to call the 'date' method
    #     time = app.scheduled_time.time()

        # Render the appointments in the template
    return render(request, 'staff/patient_appointments.html', {
        'patient': patient,
        'appointments': appointments,
    })


@login_required
def add_consultation_note(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if appointment.doctor != request.user:
        return redirect('unauthorized')

    if request.method == 'POST':
        note = request.POST.get('note')
        prescription = request.POST.get('prescription')
        treatment_plan = request.POST.get('treatment_plan')

        ConsultationNote.objects.create(
            appointment=appointment,
            doctor=request.user,
            note=note,
            prescription=prescription,
            treatment_plan=treatment_plan
        )
        return redirect('view_appointment', appointment_id=appointment.id)

    return render(request, 'staff/add_consultation_note.html', {'appointment': appointment})


@login_required
def patient_assignments(request):
    # Retrieve all the patients assigned to the logged-in doctor
    assignments = Assignment.objects.filter(doctor=request.user)
    return render(request, 'staff/patient_assignments.html', {'assignments': assignments})


@login_required
def manage_patient_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        assignment.notes = request.POST['notes']
        assignment.save()
        return redirect('patient_assignments')
    return render(request, 'staff/manage_patient_assignment.html', {'assignment': assignment})


# View to search for a patient by username or email
@login_required
def search_patient(request):
    query = request.GET.get('q', '')
    if query:
        patients = Patient.objects.filter(user__username__icontains=query) | Patient.objects.filter(user__email__icontains=query)
    else:
        patients = Patient.objects.all()
    return render(request, 'staff/search_patient.html', {'patients': patients, 'query': query})


# View to display patient details and their options (add vitals, progress tracking, etc.)
@login_required
def display_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    vitals = VitalSign.objects.filter(patient=patient)
    progress_reports = ProgressTracking.objects.filter(patient=patient)
    care_plans = CarePlan.objects.filter(patient=patient)
    medical_records = MedicalRecord.objects.filter(patient=patient)
    lab_tests = LabTest.objects.filter(patient=patient)
    prescriptions = Prescription.objects.filter(patient=patient)

    print(request.user.username)

    return render(request, 'staff/display_patient.html', {
        'patient': patient,
        'vitals': vitals,
        'progress_reports': progress_reports,
        'care_plans': care_plans,
        'medical_records': medical_records,
        'lab_tests': lab_tests,
        'prescriptions': prescriptions
    })


@login_required
def add_vitals(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        blood_pressure = request.POST['blood_pressure']
        temperature = request.POST['temperature']
        pulse = request.POST['pulse']
        weight = request.POST.get('weight', '')
        oxygen_saturation = request.POST.get('oxygen_saturation', '')

        vital_sign = VitalSign(
            patient=patient,
            blood_pressure=blood_pressure,
            temperature=temperature,
            pulse=pulse,
            weight=weight,
            oxygen_saturation=oxygen_saturation
        )

        try:
            vital_sign.full_clean()  # Validate the fields
            vital_sign.save()
            return redirect('view_vitals', patient_id=patient.id)
        except ValidationError as e:
            return render(request, 'staff/add_vitals.html', {
                'patient': patient,
                'errors': e.message_dict
            })

    return render(request, 'staff/add_vitals.html', {'patient': patient})


@login_required
def add_progress_tracking(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        progress_notes = request.POST['progress_notes']

        ProgressTracking.objects.create(
            patient=patient,
            doctor=request.user,
            progress_notes=progress_notes
        )
        return redirect('view_progress_tracking', patient_id=patient.id)
    return render(request, 'staff/add_progress_tracking.html', {'patient': patient})


@login_required
def view_vitals(request, patient_id):
    vitals = VitalSign.objects.filter(patient_id=patient_id)
    return render(request, 'view_vitals.html', {'vitals': vitals})


@login_required
def view_progress_tracking(request, patient_id):
    progress_reports = ProgressTracking.objects.filter(patient_id=patient_id)
    return render(request, 'staff/view_progress_tracking.html', {'progress_reports': progress_reports})


@login_required
def add_care_plan(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        plan_description = request.POST['plan_description']
        CarePlan.objects.create(
            patient=patient,
            doctor=request.user,
            plan_description=plan_description
        )
        return redirect('view_care_plan', patient_id=patient.id)
    return render(request, 'staff/add_care_plan.html', {'patient': patient})


@login_required
def view_care_plan(request, patient_id):
    care_plans = CarePlan.objects.filter(patient_id=patient_id)
    return render(request, 'staff/view_care_plan.html', {'care_plans': care_plans})


@login_required
def add_medical_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        diagnoses = request.POST['diagnoses']
        treatment_history = request.POST['treatment_history']
        allergies = request.POST['allergies']
        family_history = request.POST['family_history']
        medications = request.POST['medications']

        MedicalRecord.objects.create(
            patient=patient,
            diagnoses=diagnoses,
            treatment_history=treatment_history,
            allergies=allergies,
            family_history=family_history,
            medications=medications
        )
        return redirect('staff:view_medical_record', patient_id=patient.id)
    return render(request, 'staff/add_medical_record.html', {'patient': patient})


@login_required
def view_medical_record(request, patient_id):
    medical_records = MedicalRecord.objects.filter(patient_id=patient_id)
    patient = Patient.objects.get(id=patient_id)
    print(patient.user.username)
    return render(request, 'staff/view_medical_record.html', {'medical_records': medical_records,
                                                              'patient': patient})


@login_required
def order_lab_test(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        test_name = request.POST['test_name']
        LabTest.objects.create(
            patient=patient,
            test_name=test_name,
            ordered_by=request.user,
            status='ordered'
        )
        return redirect('view_lab_tests', patient_id=patient.id)
    return render(request, 'staff/order_lab_test.html', {'patient': patient})


@login_required
def view_lab_tests(request, patient_id):
    lab_tests = LabTest.objects.filter(patient_id=patient_id)
    return render(request, 'staff/view_lab_tests.html', {'lab_tests': lab_tests})


@login_required
def add_lab_result(request, lab_test_id):
    lab_test = get_object_or_404(LabTest, id=lab_test_id)
    if request.method == 'POST':
        result_data = request.POST['result_data']
        findings = request.POST['findings']
        LabResult.objects.create(
            lab_test=lab_test,
            result_data=result_data,
            findings=findings
        )
        lab_test.status = 'completed'
        lab_test.save()
        return redirect('view_lab_tests', patient_id=lab_test.patient.id)
    return render(request, 'staff/add_lab_result.html', {'lab_test': lab_test})


@login_required
def prescribe_medication(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        medication_name = request.POST['medication_name']
        dosage = request.POST['dosage']
        end_date = request.POST['end_date']
        instructions = request.POST['instructions']

        Prescription.objects.create(
            patient=patient,
            doctor=request.user,
            medication_name=medication_name,
            dosage=dosage,
            end_date=end_date,
            instructions=instructions
        )
        return redirect('view_prescriptions', patient_id=patient.id)
    return render(request, 'staff/prescribe_medication.html', {'patient': patient})


@login_required
def view_prescriptions(request, patient_id):
    prescriptions = Prescription.objects.filter(patient_id=patient_id)
    return render(request, 'staff/view_prescriptions.html', {'prescriptions': prescriptions})


@login_required
def staff_messages(request):
    staff_messages = StaffMessage.objects.all()
    return render(request, 'staff/staff_messages.html', {'messages': staff_messages})


@login_required
def send_staff_message(request):
    staff_members = Staff.objects.exclude(user=request.user)  # or any filtering logic you prefer

    for staff in staff_members:
        print(staff.user.username)

    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')  # Assuming recipient's ID is passed in the form
        message_content = request.POST.get('message_content')  # The message content from the form

        if recipient_id and message_content:
            try:
                recipient = Staff.objects.get(id=recipient_id)  # Get recipient from the ID
                sender = Staff.objects.get(user=request.user)
                
                # Create and save the message
                message = StaffMessage(sender=sender, recipient=recipient, message_content=message_content)
                message.save()

                # Success message
                messages.success(request, f"Message sent to {recipient.user.username} successfully.")
                
                # Redirect to the inbox or another page (e.g., message list)
                return redirect('staff:send_staff_message')  # Change 'staff_inbox' to the appropriate URL name
            except Staff.DoesNotExist:
                messages.error(request, "Recipient not found.")
        else:
            messages.error(request, "Please fill in all fields.")

    # Render the message sending form if GET or unsuccessful POST
    return render(request, 'staff/send_staff_message.html', {'staff_members': staff_members})


@login_required
def staff_inbox(request):
    try:
        # Get the logged-in user's staff profile
        current_staff = Staff.objects.get(user=request.user)

        # Retrieve messages for the logged-in staff member
        messages = StaffMessage.objects.filter(recipient=current_staff).order_by('-sent_at')
    except Staff.DoesNotExist:
        messages.error(request, "Staff profile not found.")
        messages = None

    # Render the inbox template
    return render(request, 'staff/staff_inbox.html', {'messages': messages})


@login_required
def message_detail(request, message_id):
    try:
        # Get the specific message
        message = StaffMessage.objects.get(id=message_id, recipient__user=request.user)

        # Mark as read if not already read
        if not message.is_read:
            message.is_read = True
            message.read_at = now()
            message.save()

        # Render the message detail template
        return render(request, 'staff/message_detail.html', {'message': message})
    except StaffMessage.DoesNotExist:
        messages.error(request, "Message not found or you do not have permission to view it.")
        return redirect('staff_inbox')  # Redirect to inbox if message not found


# request.user.staff_profile.role
@login_required
def doctor_patient_messages(request, patient_id):
    # Get the patient instance
    try:
        recipient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return render(request, 'staff/doctor_patient_messages.html', {'error': 'Patient not found'})

    # Get messages for the patient
    messages = DoctorPatientMessage.objects.filter(recipient=recipient)

    if request.method == 'POST':
        if request.user.staff_profile.role == 'doctor':  # Check if the user is a doctor
            # Initialize the form with sender (the logged-in doctor) and patient_id
            form = DoctorPatientMessageForm(request.POST, sender=request.user, patient_id=patient_id)
            if form.is_valid():
                form.save()  # Save the form
                return redirect('staff:doctor_patient_messages', patient_id=patient_id)
        else:
            return redirect('staff:permission_denied')  # Handle permission error if not a doctor
    else:
        # Initialize the form with sender (the logged-in doctor) and patient_id
        form = DoctorPatientMessageForm(sender=request.user, patient_id=patient_id)

    return render(request, 'staff/doctor_patient_messages.html', {
        'messages': messages,
        'patient_id': patient_id,
        'form': form,
        'patient': recipient
    })


@login_required
# walai i dont remember what this is for
def team_collaboration(request, patient_id):
    team_messages = TeamMessage.objects.filter(patient_id=patient_id)
    return render(request, 'staff/team_collaboration.html', {'messages': team_messages, 'patient_id': patient_id})


def insurance_verification(request, patient_id):
    try:
        # Retrieve the insurance record for the given patient if it's not verified yet
        insurance = Insurance.objects.get(profile__user__id=patient_id, verified=False)
        return render(request, 'staff/insurance_verification.html', {'insurance': insurance})
    except Insurance.DoesNotExist:
        # If no unverified insurance record is found, display an error message
        return render(request, 'staff/insurance_verification.html', {'error': 'Insurance not found or already verified'})


def verify_insurance(request, insurance_id):
    # Retrieve the insurance record by ID
    insurance = get_object_or_404(Insurance, id=insurance_id)

    # Mark the insurance as verified
    insurance.verified = True
    insurance.save()

    # Redirect to a confirmation page or back to the insurance list
    return redirect('insurance_verification', patient_id=insurance.profile.user.id)


def bill_creation_and_tracking(request, patient_id):
    patient = get_object_or_404(Profile, user__id=patient_id)  # Assuming Profile model links user to patient

    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.patient = patient
            bill.save()
            return redirect('bill_tracking', patient_id=patient.id)
    else:
        form = BillForm()

    bills = Bill.objects.filter(patient=patient)
    return render(request, 'staff/bill_tracking.html', {'bills': bills, 'form': form})


def insurance_claim_submission(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)  # Get the bill associated with the claim
    claims = InsuranceClaim.objects.filter(bill=bill)

    if request.method == 'POST':
        form = InsuranceClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.bill = bill
            claim.save()
            return redirect('insurance_claim_submission', bill_id=bill.id)
    else:
        form = InsuranceClaimForm()

    return render(request, 'staff/insurance_claim_submission.html', {'bill': bill, 'claims': claims, 'form': form})


def emergency_alert_list(request):
    # Fetch emergency alerts for the logged-in user's profile
    alerts = EmergencyAlert.objects.filter(profile=request.user.profile)
    return render(request, 'staff/emergency_alert_list.html', {'alerts': alerts})


@login_required
def acknowledge_alert(request, pk):
    alert = get_object_or_404(EmergencyAlert, pk=pk)
    alert.status = 'acknowledged'
    alert.save()
    return redirect('emergency_alert_list')


@login_required
def resolve_alert(request, pk):
    alert = get_object_or_404(EmergencyAlert, pk=pk)
    alert.status = 'resolved'
    alert.resolved_at = timezone.now()
    alert.save()
    return redirect('emergency_alert_list')


@login_required
def order_management(request):
    orders = Order.objects.all()
    return render(request, 'staff/order_management.html', {'orders': orders})


@login_required
def stock_alerts(request):
    alerts = StockAlert.objects.filter(alert_status='unresolved')
    return render(request, 'staff/stock_alerts.html', {'alerts': alerts})


@login_required
def medical_supply_inventory(request):
    supplies = MedicalSupply.objects.all()
    return render(request, 'staff/medical_supply_inventory.html', {'supplies': supplies})


@login_required
def dashboard_view(request):
    metrics = HospitalPerformanceMetrics.objects.latest('updated_at')
    analytics = PerformanceAnalytics.objects.order_by('-report_date')[:5]
    return render(request, 'staff/hospital_dashboard.html', {'metrics': metrics, 'analytics': analytics})


@login_required
def resource_allocation_view(request):
    resources = ResourceAllocation.objects.all()
    return render(request, 'staff/resource_allocation.html', {'resources': resources})


@login_required
def create_report(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        report_type = request.POST.get('report_type')
        file_path = request.FILES.get('file_path')

        report = Report.objects.create(
            title=title,
            report_type=report_type,
            generated_for=patient,
            generated_by=request.user.staff_profile,  # Assuming logged-in user is staff
            file_path=file_path,
        )
        return redirect('staff:report_list', patient_id=patient.id)

    return render(request, 'staff/create_report.html', {'patient': patient})


@login_required
def download_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return FileResponse(open(report.file_path.path, 'rb'), content_type='application/pdf')

@login_required
def report_list(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    reports = Report.objects.filter(generated_for=patient)
    return render(request, 'staff/report_list.html', {'reports': reports, 'patient': patient})

@login_required
def report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return render(request, 'staff/report_detail.html', {'report': report})


@login_required
def audit_log_list(request):
    logs = AuditLog.objects.all()
    return render(request, 'staff/audit_log_list.html', {'logs': logs})
#might give me some issues


@login_required
def audit_log_detail(request, log_id):
    log = get_object_or_404(AuditLog, id=log_id)
    return render(request, 'staff/audit_log_detail.html', {'log': log})


@login_required
# View to display all Health & Safety Protocols
def health_and_safety_protocols(request):
    protocols = HealthAndSafetyProtocol.objects.all()
    return render(request, 'staff/health_and_safety_protocols.html', {'protocols': protocols})


@login_required
# View to display all Infection Control Practices
def infection_control_practices(request):
    practices = InfectionControlPractice.objects.all()
    return render(request, 'staff/infection_control_practices.html', {'practices': practices})


@login_required
def staff_list(request):
    staff_members = Staff.objects.all()  # Get all staff members
    return render(request, 'staff/staff_list.html', {'staff': staff_members})


@login_required
def staff_certifications(request, staff_id):
    staff_member = get_object_or_404(Staff, id=staff_id)  # Get the staff member by ID
    certifications = staff_member.certifications.all()  # Get the certifications for that staff member
    return render(request, 'staff/staff_certifications.html', {'staff_member': staff_member, 'certifications': certifications})


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'staff/notifications.html', {'notifications': notifications})

