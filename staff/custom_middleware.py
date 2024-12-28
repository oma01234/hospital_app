from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.urls import resolve


def dynamic_login_url(request):
    if request.path.startswith('/staff/') and not request.path.startswith('/staff/api/'):
        request.login_url = reverse('staff:login')  # staff login URL
    else:
        request.login_url = settings.LOGIN_URL  # Default login URL

class DynamicLoginURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        dynamic_login_url(request)  # Call the request processor
        response = self.get_response(request)
        return response


class StaffOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Resolve the current request to get the URL name
        resolver_match = resolve(request.path)
        url_name = resolver_match.url_name  # The name of the resolved URL

        # Allow access to the 'login' URL without restrictions
        if url_name == 'login' or url_name == 'register' :  # Match the name defined in your URL pattern
            return self.get_response(request)

        # Restrict access to staff-only URLs
        if request.user.is_authenticated and request.user.groups.filter(name="staff").exists():
            return self.get_response(request)
        else:
            return HttpResponseForbidden("Access denied.")
