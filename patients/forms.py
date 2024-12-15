from django import forms
from django.contrib.auth.models import User
from .models import *

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'emergency_contact', 'medical_history', 'allergies', 'insurance_details']

class MedicationReminderForm(forms.ModelForm):
    class Meta:
        model = MedicationReminder
        fields = ['medication_name', 'dosage', 'time', 'reminder_text']

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['total_amount', 'paid_amount', 'due_date', 'is_paid']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
