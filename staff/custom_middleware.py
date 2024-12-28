from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.urls import resolve, reverse
from staff.models import Staff


def dynamic_login_url(request):
    if request.path.startswith('/staff/'):
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


# class StaffOnlyMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # Resolve the current request to get the URL name
#         resolver_match = resolve(request.path)
#         url_name = resolver_match.url_name  # The name of the resolved URL
#
#         # Allow access to the 'login' URL without restrictions
#         if url_name == 'login' or url_name == 'register' :  # Match the name defined in your URL pattern
#             return self.get_response(request)
#
#         # Restrict access to staff-only URLs
#         if request.user.is_authenticated:
#             try:
#                 # Check if the user has an entry in the Staff model
#                 if Staff.objects.filter(user=request.user).exists():
#                     print("User is a staff member.")
#                     return self.get_response(request)
#                 else:
#                     print("User is not a staff member.")
#             except Staff.DoesNotExist:
#                 print("Staff entry does not exist for this user.")
#         else:
#             print("User is not authenticated.")
#
#             # Deny access if conditions are not met
#         return HttpResponseForbidden("Access denied. Staff members only.")


class StaffOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Resolve the current request to get the URL namespace
        resolver_match = resolve(request.path)
        url_name = resolver_match.url_name
        app_name = resolver_match.app_name  # The namespace of the URL

        # Allow access to non-'staff' URLs without restrictions
        if app_name != 'staff':  # Replace 'staff' with your actual app_name if different
            return self.get_response(request)

        if url_name == 'login' or url_name == 'register' :  # Match the name defined in your URL pattern
            return self.get_response(request)

        # Check if the user is authenticated and is in the Staff model
        if request.user.is_authenticated:
            try:
                Staff.objects.get(user=request.user)
                # User is a staff member, allow the request
                return self.get_response(request)
            except Staff.DoesNotExist:
                # User is not a staff member
                return HttpResponseForbidden("Access denied. Staff members only.")

        # If the user is not authenticated
        return HttpResponseForbidden("Access denied. Please log in.")