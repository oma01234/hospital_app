from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from staff.models import DoctorPatientMessage, Report
from django.contrib import messages
from django.http import FileResponse


def landing(request):

    return render(request, 'patients/landing.html')


# Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save User model fields
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create the Patient instance linked to the User
            patient, created = Patient.objects.get_or_create(user=user)

            if not created:
                # Patient instance already exists
                print('Patient already exists')
                return redirect('patients:register')

            # Save Profile model fields
            Profile.objects.create(
                user=patient,
                phone_number=form.cleaned_data.get('phone_number'),
                emergency_contact=form.cleaned_data.get('emergency_contact'),
                medical_history=form.cleaned_data.get('medical_history'),
                allergies=form.cleaned_data.get('allergies'),
                insurance_details=form.cleaned_data.get('insurance_details'),
            )

            return redirect('patients:login')
    else:
        form = UserRegistrationForm()

    return render(request, 'patients/register.html', {'form': form})


# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                print('logged in')
                return redirect('patients:home')
    else:
        form = LoginForm()
    return render(request, 'patients/login.html', {'form': form})


def logout_view(request):
    # Check if the logged-in user has a Profile (i.e., is a patient)
    try:
        # Attempt to access the Profile using the related_name 'profile'
        profile = request.user.Patient.profile  # This will raise an exception if no Profile exists

        # If the user has a Profile, they are a patient
        logout(request)
        return redirect('patients:login')

    except ObjectDoesNotExist:
        # If no Profile exists for the user, they are not a patient
        logout(request)


@login_required
def home(request):

    return render(request, 'patients/home.html')


@login_required
# Profile View
def profile(request):

    view_profile = get_object_or_404(Profile, user=request.user.Patient)

    return render(request, 'patients/profile.html', {'profile': view_profile})


@login_required
def update_profile(request):
    profile = get_object_or_404(Profile, user=request.user.Patient)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            # Save the form and automatically set `modified_by` in the signal
            form.save()
            return redirect('patients:profile')  # Redirect to profile page after saving
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'patients/update_profile.html', {'form': form, 'profile': profile})


@login_required
def medication_reminders(request):
    reminders = MedicationReminder.objects.filter(patient=request.user.Patient)
    return render(request, 'appointments/medication_reminders.html', {'reminders': reminders})


@login_required
# def bill_list(request):
#     bills = Bill.objects.filter(patient=request.user)
#     return render(request, 'appointments/bill_list.html', {'bills': bills})


@login_required
def feedback_form(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)  # Create a feedback instance but don't save yet
            feedback.patient = request.user.patient  # Assign the patient
            feedback.save()  # Now save the instance
            return redirect('appointments:feedback_submitted')
    else:
        form = FeedbackForm()
    return render(request, 'appointments/feedback_form.html', {'form': form})


# Treatment Plans View
@login_required
def treatment_plans(request):
    plans = TreatmentPlan.objects.filter(patient=request.user.Patient)
    return render(request, 'appointments/treatment_plans.html', {'plans': plans})


# Emergency Contact View
@login_required
def emergency_contact(request):
    emergency_service = EmergencyService.objects.filter(patient=request.user.Patient).first()  # Assuming only one service request per patient
    return render(request, 'appointments/emergency_contact.html', {'emergency_service': emergency_service})


# This is for the patient viewing messages
@login_required
def patient_messages(request):
    messages = DoctorPatientMessage.objects.filter(recipient_id=request.user.Patient.id)
    if messages:
        print('message')
    else:
        print('crazy')
    for message in messages:
        print(message, 'jjjj')
    return render(request, 'patients/patient_messages.html', {'messages': messages})


@login_required
def view_message(request, message_id):
    # Get the specific message
    message = get_object_or_404(DoctorPatientMessage, id=message_id)

    # Ensure only the recipient (patient) can view and reply
    if message.recipient.user != request.user:
        messages.error(request, "You are not authorized to view this message.")
        return redirect('patients:login')  # Redirect to the patient's inbox

    if request.method == 'POST':
        reply_content = request.POST.get('patient_reply')  # Get the reply from the form

        if reply_content:
            message.patient_reply = reply_content  # Save the reply
            message.save()
            messages.success(request, "Your reply has been sent.")
            return redirect('patients:patient_messages')  # Redirect back to inbox or messages list
        else:
            messages.error(request, "Reply content cannot be empty.")

    return render(request, 'patients/view_messages.html', {'message': message})


@login_required
def download_report(request, report_id):
    # Ensure the logged-in patient can only access their reports
    report = get_object_or_404(Report, id=report_id, generated_for=request.user.patient)
    return FileResponse(open(report.file_path.path, 'rb'), content_type='application/pdf')


@login_required
def report_list(request):
    # Filter reports to show only those belonging to the logged-in patient
    patient = request.user.Patient  # Assuming `request.user` is linked to a `Patient` profile
    reports = Report.objects.filter(generated_for=patient)
    return render(request, 'patients/report_list.html', {'reports': reports})


@login_required
def report_detail(request, report_id):
    # Ensure the logged-in patient can only view details of their reports
    report = get_object_or_404(Report, id=report_id, generated_for=request.user.patient)
    return render(request, 'patients/report_detail.html', {'report': report})