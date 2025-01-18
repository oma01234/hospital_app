# permissions.py
from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.staff.role == 'doctor'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.staff.role == 'admin'


class IsStaffMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            print("Permission Denied: User not authenticated")
            return False
        if not hasattr(request.user, 'staff_profile'):
            print("Permission Denied: User has no staff profile")
            return False
        if request.user.staff_profile.role not in ['doctor', 'nurse', 'admin']:
            print(f"Permission Denied: Invalid role {request.user.staff_profile.role}")
            return False
        print(f"Permission Granted: User {request.user} with role {request.user.staff_profile.role}")
        return True