from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *

def landing(request):

    return render(request, 'patients/landing.html')

# Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
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
                return redirect('patients:profile')
    else:
        form = LoginForm()
    return render(request, 'patients/login.html', {'form': form})


def home(request):

    return render(request, 'patients/home.html')

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


def medication_reminders(request):
    reminders = MedicationReminder.objects.filter(patient=request.user)
    return render(request, 'appointments/medication_reminders.html', {'reminders': reminders})

def bill_list(request):
    bills = Bill.objects.filter(patient=request.user)
    return render(request, 'appointments/bill_list.html', {'bills': bills})

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
def treatment_plans(request):
    plans = TreatmentPlan.objects.filter(patient=request.user)
    return render(request, 'appointments/treatment_plans.html', {'plans': plans})

# Emergency Contact View
def emergency_contact(request):
    emergency_service = EmergencyService.objects.filter(patient=request.user).first()  # Assuming only one service request per patient
    return render(request, 'appointments/emergency_contact.html', {'emergency_service': emergency_service})
