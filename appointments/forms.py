from django import forms
from .models import *

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
    
    def __init__(self, *args, **kwargs):
        # Ensure you have access to the patient when creating the form
        self.patient = kwargs.get('patient', None)
        super().__init__(*args, **kwargs)

        # Filter the doctor queryset to only show doctors
        self.fields['doctor'].queryset = Staff.objects.filter(role='doctor')

        # Optionally, if you want to filter doctors based on the patient's assigned doctor(s)
        if self.patient:
            # You can filter doctors based on a specific patient’s prior assignments (optional)
            # For example: show doctors that the patient has been assigned to before
            self.fields['doctor'].queryset = self.fields['doctor'].queryset.filter(assignments__patient=self.patient)


class ConsultationNoteForm(forms.ModelForm):
    class Meta:
        model = ConsultationNote
        fields = ['notes']
