from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_profiles import (
    UserViewSet, TenantProfileViewSet, ManagerProfileViewSet,
    LandlordProfileViewSet, LandlordPayoutMethodViewSet,
    PropertyManagerViewSet)
from .views_permissions import(
    PermissionViewSet, RolePermissionViewSet, UserPermissionViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename="users")
router.register(r'tenants', TenantProfileViewSet, basename="tenant-profiles")
router.register(r'managers', ManagerProfileViewSet, basename="manager-profiles")
router.register(r'landlords', LandlordProfileViewSet, basename="landlord-profiles")
router.register(r'payout-methods', LandlordPayoutMethodViewSet, basename="landlord-payout-methods")
router.register(r'property-managers', PropertyManagerViewSet, basename="property-managers")
router.register(r'permissions', PermissionViewSet, basename="permissions")
router.register(r'role-permissions', RolePermissionViewSet, basename="role-permissions")
router.register(r'user-permissions', UserPermissionViewSet, basename="user-permissions")

urlpatterns = [
    path("", include(router.urls)),
]
