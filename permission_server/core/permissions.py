from rest_framework import permissions
from .models import Role

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Role.ADMIN

class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in [Role.MANAGER, Role.ADMIN]

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS