from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

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


