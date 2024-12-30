from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve, reverse
from .models import Patient
from django.http import HttpResponseForbidden

def dynamic_login_url(request):
    """
    Sets the login URL based on the requested URL.
    """
    if request.path.startswith('/patients/'):
        request.login_url = reverse('patients:login')  # Patients login URL
    else:
        request.login_url = settings.LOGIN_URL  # Default login URL

class DynamicLoginURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        dynamic_login_url(request)  # Call the request processor
        response = self.get_response(request)
        return response


class PatientOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Resolve the current request to get the URL namespace
        resolver_match = resolve(request.path)
        url_name = resolver_match.url_name
        app_name = resolver_match.app_name  # The namespace of the URL

        # Allow access to non-'staff' URLs without restrictions
        if app_name != 'patients':
            return self.get_response(request)

        if url_name == 'login' or url_name == 'register' or url_name == 'landing' or url_name == 'logout' :  # Match the name defined in your URL pattern
            return self.get_response(request)

        # Check if the user is authenticated and is in the Patient model
        if request.user.is_authenticated:
            try:
                Patient.objects.get(user=request.user)
                # User is a patient member, allow the request
                return self.get_response(request)
            except Patient.DoesNotExist:
                # User is not a staff member
                return HttpResponseForbidden("Access denied. Patients only.")

        # If the user is not authenticated
        return HttpResponseForbidden("Access denied. Please log in.")

