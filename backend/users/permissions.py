from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import Permission as AppPermission, RolePermission, User, TenantProfile, ManagerProfile, LandlordProfile, PropertyManager, UserPermission
import logging



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

class RBACPermission(BasePermission):
    """
    Custom RBAC permission system based on:
      - User roles (tenant, landlord, manager, admin)
      - User/Role permissions (future-proof for dynamic codes)
      - Object-level ownership
    """

    def has_permission(self, request, view):
        """Global permission check before hitting object-level logic"""
        user = request.user
        if not user.is_authenticated:
            return False

        #Admin can do everything
        if user.is_superuser or user.is_admin:
            return True
        
        # Example: Only admins can CRUD Permission/RolePermission/UserPermission models
         # Restrict Permission-related models
        if view.queryset.model in [AppPermission, RolePermission, UserPermission]:
            return False  # 👈 non-admins cannot access
        
        # Dynamic permission check
        required_permission = getattr(view, "required_permission", None)
        if required_permission:
            return self._check_dynamic_permission(user, required_permission)
        
        return True
    
    def has_object_permission(self, request, view, obj):
        """Object-level checks for profiles and assignments"""
        user = request.user

        #Admin can do everything
        if user.is_superuser or user.is_admin:
            return True
        
        # ---------------- TENANT PROFILE ----------------
        if isinstance(obj, TenantProfile):
           
            if view.action in ["retrieve", "update", "partial_update"]:
                if user.is_tenant and obj.user == user:
                    return True
                if user.is_manager and hasattr(user, "landlord_profile"):
                    return True
                return False

            if view.action == "destroy":
                if user.is_manager and user.landlord_profile:
                    return True  # landlord can delete tenants
                return False
            
            if view.action == "restore_profile":
                if user.landlord_profile:
                    return True  # landlord restores tenants
            return False

        # ---------------- MANAGER PROFILE ----------------
        if isinstance(obj, ManagerProfile):
            if user.is_manager and obj.user == user:
                return True
            if user.is_manager and user.landlord_profile:
                return True
            return False
        
        # ---------------- LANDLORD PROFILE ----------------
        if isinstance(obj, LandlordProfile):
            return user == obj.manager.user
        
        # ---------------- PROPERTY MANAGER ASSIGNMENTS ----------------
        if isinstance(obj, PropertyManager):
            if user == obj.user:
                return True
            if user.is_manager and user.landlord_profile:
                return True
            return False

        return False

    def _check_dynamic_permission(self, user, permission_code, property_id=None):
        """Check RolePermission + UserPermission for dynamic access"""
        # Role defaults
        role = getattr(getattr(user, "manager_profile", None), "role", None)
        role_perms = set(
            RolePermission.objects.filter(role=role).values_list("permission__code", flat=True)
        )if role else set()

        # User-specific global
        # user_global = set(
        #     UserPermission.objects.filter(user=user, property__isnull=True)
        #     .values_list("permission_code", flat=True)
        # )

        user_global = set(
            UserPermission.objects.filter(user=user)
            .values_list("permission__code", flat=True)
        )

        # User-specific property scoped
        # user_property = set()
        # if property_id:
        #     user_property = set(
        #         UserPermission.objects.filter(user=user,property_id=property_id)
        #         .values_list("permission__code",flat=True)
        #     )
        
        effective = role_perms | user_global
        # effective = role_perms | user_global | user_property
        return permission_code in effective