from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
from .models import *
from .forms import *
from django.contrib import messages
from staff.models import Staff

now = datetime.now()
today = now.date()

@login_required
def book_appointment(request):
    doctors = Staff.objects.filter(role='doctor')
    for doctor in doctors:
        print(doctor)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, patient=request.user.Patient)  # Pass the logged-in user (patient) to the form
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.Patient  # Set the patient explicitly to the logged-in user
            appointment.save()
            return redirect('appointments:appointment_list')  # Redirect to the appointment list or another page
    else:
        print(request.user.Patient, "hrdyrxjty")
        form = AppointmentForm(patient=request.user.Patient)  # Pass the logged-in user (patient) to the form
    
    return render(request, 'appointments/book_appointment.html', {'form': form})


@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(patient=request.user.Patient)

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        action = request.POST.get('action')

        if appointment_id and action:
            appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.Patient)

            if action == 'cancel':
                appointment.status = 'Cancelled'
                appointment.save()
                messages.success(request, "Appointment successfully cancelled.")

            elif action == 'reschedule':
                form = RescheduleAppointmentForm(request.POST)
                if form.is_valid():
                    appointment.status = 'Rescheduled'
                    appointment.reschedule_request_date = form.cleaned_data['new_date']
                    appointment.reschedule_request_time = form.cleaned_data['new_time']
                    appointment.save()
                    messages.success(request, "Reschedule request submitted successfully.")
                else:
                    messages.error(request, "Invalid reschedule request.")

            return redirect('appointments:appointment_list')

    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})


@login_required
def consultation_history(request):
    past_appointments = Appointment.objects.filter(patient=request.user.Patient, date__lt=today)
    upcoming_appointments = Appointment.objects.filter(patient=request.user.Patient, date__lt=today)
    return render(request, 'appointments/consultation_history.html', {
        'past_appointments': past_appointments,
        'upcoming_appointments': upcoming_appointments,
    })


@login_required
def book_virtual_consultation(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.Patient
            appointment.consultation_type = 'Virtual'
            appointment.save()
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book_virtual_consultation.html', {'form': form})


@login_required
def add_consultation_note(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = ConsultationNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.appointment = appointment
            note.save()
            return redirect('appointments:appointment_list')
    else:
        form = ConsultationNoteForm()
    return render(request, 'appointments/add_consultation_note.html', {'form': form, 'appointment': appointment})
