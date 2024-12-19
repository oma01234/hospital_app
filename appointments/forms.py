from django import forms
from .models import *

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        # set the doctor field to automatically set the doctor assigned to the patient
        fields = ['doctor', 'date', 'time', 'reason']


class ConsultationNoteForm(forms.ModelForm):
    class Meta:
        model = ConsultationNote
        fields = ['notes']