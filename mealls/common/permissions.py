from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        return True
