from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrStaffOrReadOnly(BasePermission):

    def has_object_permission(self, request, _, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            (request.user.is_authenticated and request.user ==
             obj.owner or request.user.is_staff)
        )
