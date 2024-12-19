from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required


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

            # Check if the profile already exists
            profile, created = Profile.objects.get_or_create(user=user)
            if not created:
                # Profile already exists, pass a message
                print('created already')

                # Redirect to the same page to start the process again (or another page)
                return redirect('patients:register')

            # Save Profile model fields only if it's a new profile
            Profile.objects.create(
                user=user,
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
                return redirect('patients:home')
    else:
        form = LoginForm()
    return render(request, 'patients/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('patients:login')


@login_required
def home(request):

    return render(request, 'patients/home.html')

@login_required
# Profile View
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'patients/profile.html', {'form': form})


@login_required
def medication_reminders(request):
    reminders = MedicationReminder.objects.filter(patient=request.user)
    return render(request, 'appointments/medication_reminders.html', {'reminders': reminders})


@login_required
def bill_list(request):
    bills = Bill.objects.filter(patient=request.user)
    return render(request, 'appointments/bill_list.html', {'bills': bills})


@login_required
def feedback_form(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save(patient=request.user)
            return redirect('appointments:feedback_submitted')
    else:
        form = FeedbackForm()
    return render(request, 'appointments/feedback_form.html', {'form': form})


# Treatment Plans View
@login_required
def treatment_plans(request):
    plans = TreatmentPlan.objects.filter(patient=request.user)
    return render(request, 'appointments/treatment_plans.html', {'plans': plans})


# Emergency Contact View
@login_required
def emergency_contact(request):
    emergency_service = EmergencyService.objects.filter(patient=request.user).first()  # Assuming only one service request per patient
    return render(request, 'appointments/emergency_contact.html', {'emergency_service': emergency_service})
