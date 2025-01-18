from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve, reverse
from .models import Patient
from django.http import HttpResponseForbidden
from rest_framework_simplejwt.authentication import JWTAuthentication


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
        app_name = resolver_match.app_name

        # Allow access to non-patient URLs without restrictions
        if app_name != 'patients':
            return self.get_response(request)

        # Allow access to specific endpoints like login and register
        if url_name in ['login', 'register', 'api_register', 'api_login']:
            return self.get_response(request)

        # Authenticate using JWT
        jwt_auth = JWTAuthentication()
        auth_result = jwt_auth.authenticate(request)
        print(auth_result, "nawa")

        if auth_result:
            user, token = auth_result
            # Check if the user is associated with a Patient instance
            if user:
                return self.get_response(request)

        return HttpResponseForbidden("You must be a patient to access this resource uayua.")


