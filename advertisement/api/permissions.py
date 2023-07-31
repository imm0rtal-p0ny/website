from rest_framework import permissions
from board.models import Status


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsAuthorized(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return bool(request.user.is_authorized)
        return False


class IsOwnerOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated and request.user.is_authorized:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user == obj.user or request.user.is_superuser)


class UserRegisterUpdatePermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj or request.user.is_superuser


class UserAuthenticatedAndNotAuthorized(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and not request.user.is_authorized:
            return True
        return False



