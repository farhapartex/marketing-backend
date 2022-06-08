from rest_framework import permissions
from user import constants


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == constants.RoleType.admin
