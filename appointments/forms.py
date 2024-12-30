from django import forms
from .models import *
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
        widgets = {
            'date': forms.TextInput(attrs={'id': 'date-picker'}),
            'time': forms.TextInput(attrs={'id': 'time-picker'}),
        }

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)  # Get the patient from kwargs
        super().__init__(*args, **kwargs)

        # Filter the doctor queryset to show only assigned doctors for the patient
        if self.patient:
            self.fields['doctor'].queryset = Staff.objects.filter(
                role='doctor',
            ).distinct()


class ConsultationNoteForm(forms.ModelForm):
    class Meta:
        model = ConsultationNote
        fields = ['notes']


class RescheduleAppointmentForm(forms.Form):
    new_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    new_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))