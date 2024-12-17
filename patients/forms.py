from django import forms
from django.contrib.auth.models import User
from .models import *


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # Fields for Profile model


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return confirm_password


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
