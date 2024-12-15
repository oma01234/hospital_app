from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
import re
from django.core.exceptions import ValidationError


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['item_description', 'quantity', 'unit_price', 'total_amount', 'status']


class InsuranceClaimForm(forms.ModelForm):
    class Meta:
        model = InsuranceClaim
        fields = ['claim_number', 'status']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'emergency_contact', 'medical_history', 'allergies', 'insurance_details']


class StaffUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=Staff.ROLE_CHOICES, label="Role")
    specialty = forms.CharField(max_length=100, required=False, label="Specialty (Doctors Only)")
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    profile_picture = forms.ImageField(required=False, label="Profile Picture")

    class Meta:
        model = Staff
        fields = ('username', 'email', 'password1', 'password2', 'role', 'specialty', 'phone_number', 'profile_picture')

    def save(self, commit=True):
        staff = super().save(commit=False)

        # Add any additional processing before saving
        staff.role = self.cleaned_data['role']
        staff.specialty = self.cleaned_data.get('specialty', '')
        staff.phone_number = self.cleaned_data['phone_number']
        staff.profile_picture = self.cleaned_data.get('profile_picture', None)

        if commit:
            staff.save()

        return staff

