from django import forms
from .models import *
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


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



class StaffUserCreationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
        label="Username"
    )
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    role = forms.ChoiceField(choices=Staff.ROLE_CHOICES, label="Role")
    specialty = forms.CharField(required=False, label="Specialty")  # Optional for non-doctors
    phone_number = forms.CharField(label="Phone Number")
    profile_picture = forms.ImageField(required=False, label="Profile Picture")

    class Meta:
        model = Staff
        fields = ['role', 'specialty', 'phone_number', 'profile_picture']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.replace(" ", "").isalnum():
            raise forms.ValidationError("Username can only contain letters, numbers, and spaces.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        # Create the user first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )

        # Save the staff model with the user and role information
        staff = super().save(commit=False)
        staff.user = user  # Link to User model
        staff.role = self.cleaned_data['role']  # Assign the role to Staff model
        if commit:
            staff.save()
        return staff




