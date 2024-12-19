from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

class DynamicLoginURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Dynamically adjust the login URL based on the app namespace
        if request.path.startswith('/patients/'):
            print('Here is the patients app')
            settings.LOGIN_URL = reverse('patients:login')  # Patients login URL
        else:
            pass  # Add more conditions if needed for other apps like staff

        response = self.get_response(request)
        return response

