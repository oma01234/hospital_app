from django import forms
from .models import *

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']

    def __init__(self, *args, **kwargs):
        self.patient = kwargs.pop('patient', None)  # Get the patient from kwargs
        super().__init__(*args, **kwargs)

        # Filter the doctor queryset to show only assigned doctors for the patient
        if self.patient:
            self.fields['doctor'].queryset = Staff.objects.filter(
                role='doctor',
                doctor_assignments__patient=self.patient
            ).distinct()


class ConsultationNoteForm(forms.ModelForm):
    class Meta:
        model = ConsultationNote
        fields = ['notes']
