# permissions.py
from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.staff.role == 'doctor'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.staff.role == 'admin'
