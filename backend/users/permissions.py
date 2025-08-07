from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsAuthenticatedAndActive(BasePermission):
    """
        Allows access only to users who are active.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False
        
        if not user.is_active:
            raise PermissionDenied(detail="Your account is inactive. Please contact support.")

        return True
