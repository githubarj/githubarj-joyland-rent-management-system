from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext_lazy as _

from .models import Property, Unit, Lease
from .serializers import PropertySerializer, UnitSerializer, LeaseSerializer
from users.permissions import IsAuthenticatedAndActive
from users.utils import api_response

from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from users.models import PropertyManager
from .access import user_has_permission, user_can_access_property_id

from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from rest_framework.exceptions import PermissionDenied, ValidationError

PROPERTY_PERMISSION_MAP = {
    "list": "can_view_properties",
    "retrieve": "can_view_properties",
    "create": "can_manage_properties",
    "update": "can_manage_properties",
    "partial_update": "can_manage_properties",
    "destroy": "can_manage_properties",
}

UNIT_PERMISSION_MAP = {
    "list": "can_view_units",
    "retrieve": "can_view_units",
    "create": "can_manage_units",
    "update": "can_manage_units",
    "partial_update": "can_manage_units",
    "destroy": "can_manage_units",
}

LEASE_PERMISSION_MAP = {
    "list": "can_view_leases",
    "retrieve": "can_view_leases",
    "create": "can_manage_leases",
    "update": "can_manage_leases",
    "partial_update": "can_manage_leases",
    "destroy": "can_manage_leases",
}


# Assumes these constants and mixins are imported from your custom security framework
# from core.permissions import DynamicPermissionMixin, IsAuthenticatedAndActive
# from core.constants import PROPERTY_PERMISSION_MAP

from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError

# Assumes custom helpers, mixins, and constants are imported correctly
# from .utils import user_can_access_property_id
# from core.permissions import DynamicPermissionMixin, IsAuthenticatedAndActive
# from core.constants import PROPERTY_PERMISSION_MAP

class PropertyViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedAndActive]
    permission_map = PROPERTY_PERMISSION_MAP

    def get_queryset(self):
        user = self.request.user

        # Base optimization: Cache the landlord join early to avoid N+1 issues
        base_queryset = Property.objects.filter(deleted_at__isnull=True).select_related("landlord")

        # Multi-Tenant Workspace Role Isolation Strategy
        if user.is_superuser or getattr(user, "is_admin", False):
            scoped_queryset = base_queryset
        elif getattr(user, "is_manager", False):
            scoped_queryset = base_queryset.filter(
                Q(landlord=user) |
                Q(
                    managers__user=user,
                    managers__is_active=True,
                    managers__deleted_at__isnull=True,
                )
            ).distinct()
        else:
            # Tenants do not access the complete index by default
            scoped_queryset = Property.objects.none()

        # Sanitize query parameters
        params = self.request.query_params
        city = params.get("city")
        is_active = params.get("is_active")
        landlord = params.get("landlord")
        search = params.get("search")

        if city:
            scoped_queryset = scoped_queryset.filter(city__icontains=city)

        if is_active is not None:
            # FIX: Evaluates against a list to avoid false-negative filters when None
            scoped_queryset = scoped_queryset.filter(is_active=is_active.lower() in ["true", "1"])

        if landlord:
            # VALIDATION: Guardrail against ValueError database crashes
            if not landlord.isdigit():
                raise ValidationError({"landlord": _("Invalid landlord ID format.")})
            scoped_queryset = scoped_queryset.filter(landlord_id=landlord)

        if search:
            scoped_queryset = scoped_queryset.filter(name__icontains=search)

        return scoped_queryset.order_by("-created_at")

    @swagger_auto_schema(operation_summary="List properties", tags=["Properties"])
    def list(self, request, *args, **kwargs):
        self.check_dynamic_permission()
        response = super().list(request, *args, **kwargs)
        # FIX: Added required positional arguments to bypass wrapper parameter issues
        return api_response(True, "Properties fetched successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create property", request_body=PropertySerializer, tags=["Properties"])
    def create(self, request, *args, **kwargs):
        self.check_dynamic_permission()

        if not (request.user.is_superuser or getattr(request.user, "is_admin", False)):
            landlord_id = request.data.get("landlord")
            if landlord_id and int(landlord_id) != request.user.id:
                raise PermissionDenied(_("You can only create properties under your own landlord account."))

        response = super().create(request, *args, **kwargs)
        return api_response(True, "Property created successfully", response.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_summary="Retrieve property", tags=["Properties"])
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_dynamic_permission(property_id=obj.id)
        response = super().retrieve(request, *args, **kwargs)
        return api_response(True, "Property fetched successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update property", request_body=PropertySerializer, tags=["Properties"])
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_dynamic_permission(property_id=obj.id)
        response = super().update(request, *args, **kwargs)
        return api_response(True, "Property updated successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Partially update property", request_body=PropertySerializer, tags=["Properties"])
    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_dynamic_permission(property_id=obj.id)
        response = super().partial_update(request, *args, **kwargs)
        return api_response(True, "Property updated successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Soft delete property", tags=["Properties"])
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_dynamic_permission(property_id=obj.id)
        obj.soft_delete()
        return api_response(True, "Property deleted successfully", None, status.HTTP_200_OK)



from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError

# Assumes custom helpers, mixins, and constants are imported correctly
# from .utils import user_can_access_property_id
# from core.permissions import DynamicPermissionMixin, IsAuthenticatedAndActive
# from core.constants import UNIT_PERMISSION_MAP

class UnitViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticatedAndActive]
    permission_map = UNIT_PERMISSION_MAP

    def get_queryset(self):
        user = self.request.user

        # Base optimization: Joint prefetching strategy
        base_queryset = Unit.objects.filter(deleted_at__isnull=True).select_related(
            "property", "property__landlord"
        )

        if user.is_superuser or getattr(user, "is_admin", False):
            scoped_queryset = base_queryset
        elif getattr(user, "is_manager", False):
            scoped_queryset = base_queryset.filter(
                Q(property__landlord=user) |
                Q(
                    property__managers__user=user,
                    property__managers__is_active=True,
                    property__managers__deleted_at__isnull=True,
                )
            ).distinct()
        else:
            scoped_queryset = Unit.objects.none()

        params = self.request.query_params
        property_id = params.get("property")
        status_param = params.get("status")
        unit_type = params.get("unit_type")
        is_active = params.get("is_active")
        search = params.get("search")

        if property_id:
            if not property_id.isdigit():
                raise ValidationError({"property": _("Invalid property ID format.")})
            scoped_queryset = scoped_queryset.filter(property_id=property_id)

        if status_param:
            scoped_queryset = scoped_queryset.filter(status=status_param)

        if unit_type:
            scoped_queryset = scoped_queryset.filter(unit_type=unit_type)

        if is_active is not None:
            scoped_queryset = scoped_queryset.filter(is_active=is_active.lower() in ["true", "1"])

        if search:
            scoped_queryset = scoped_queryset.filter(unit_number__icontains=search)

        return scoped_queryset.order_by("property_id", "unit_number")

    @swagger_auto_schema(operation_summary="List units", tags=["Units"])
    def list(self, request, *args, **kwargs):
        self.check_dynamic_permission()
        response = super().list(request, *args, **kwargs)
        return api_response(True, "Units fetched successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create unit", request_body=UnitSerializer, tags=["Units"])
    def create(self, request, *args, **kwargs):
        property_id = request.data.get("property")

        if not property_id:
            raise ValidationError({"property": _("Property is required to create a unit.")})

        # Ensure value is converted properly for downstream utility integer evaluations
        if str(property_id).isdigit():
            property_id = int(property_id)

        # 1. Framework Permission Map Check
        self.check_dynamic_permission(property_id=property_id)

        # 2. Contextual Access Helper Integration
        if not user_can_access_property_id(request.user, property_id):
            raise PermissionDenied(_("You do not have access to this property."))

        response = super().create(request, *args, **kwargs)
        return api_response(True, "Unit created successfully", response.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_summary="Retrieve unit", tags=["Units"])
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_dynamic_permission(property_id=obj.property_id)
        response = super().retrieve(request, *args, **kwargs)
        return api_response(True, "Unit fetched successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update unit", request_body=UnitSerializer, tags=["Units"])
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_dynamic_permission(property_id=obj.property_id)
        response = super().update(request, *args, **kwargs)
        return api_response(True, "Unit updated successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Partially update unit", request_body=UnitSerializer, tags=["Units"])
    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_dynamic_permission(property_id=obj.property_id)
        response = super().partial_update(request, *args, **kwargs)
        return api_response(True, "Unit updated successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Soft delete unit", tags=["Units"])
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_dynamic_permission(property_id=obj.property_id)
        obj.soft_delete()
        return api_response(True, "Unit deleted successfully", None, status.HTTP_200_OK)

from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError

# Assumes custom helpers, mixins, and constants are imported correctly
# from .utils import user_can_access_property_id
# from core.permissions import DynamicPermissionMixin, IsAuthenticatedAndActive
# from core.constants import LEASE_PERMISSION_MAP

class LeaseViewSet(DynamicPermissionMixin, viewsets.ModelViewSet):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticatedAndActive]
    permission_map = LEASE_PERMISSION_MAP

    def get_queryset(self):
        user = self.request.user
        base_queryset = Lease.objects.filter(deleted_at__isnull=True)

        # 1. Multi-Tenant Role Isolation Strategy
        if user.is_superuser or getattr(user, "is_admin", False):
            scoped_queryset = base_queryset
        elif getattr(user, "is_tenant", False):
            scoped_queryset = base_queryset.filter(tenant=user)
        elif getattr(user, "is_manager", False):
            scoped_queryset = base_queryset.filter(
                Q(unit__property__landlord=user) |
                Q(
                    unit__property__managers__user=user,
                    unit__property__managers__is_active=True,
                    unit__property__managers__deleted_at__isnull=True,
                )
            ).distinct()
        else:
            scoped_queryset = Lease.objects.none()

        # 2. Extract and Sanitize Parameters Safely (Prevents ValueError Crashes)
        params = self.request.query_params
        tenant = params.get("tenant")
        unit = params.get("unit")
        property_id = params.get("property")
        status_param = params.get("status")

        if tenant:
            if not tenant.isdigit():
                raise ValidationError({"tenant": _("Invalid tenant ID format.")})
            scoped_queryset = scoped_queryset.filter(tenant_id=tenant)

        if unit:
            if not unit.isdigit():
                raise ValidationError({"unit": _("Invalid unit ID format.")})
            scoped_queryset = scoped_queryset.filter(unit_id=unit)

        if property_id:
            if not property_id.isdigit():
                raise ValidationError({"property": _("Invalid property ID format.")})
            scoped_queryset = scoped_queryset.filter(unit__property_id=property_id)

        if status_param:
            scoped_queryset = scoped_queryset.filter(status=status_param)

        # 3. Optimized Database Joins Fetching Last
        return scoped_queryset.select_related(
            "tenant", "unit", "unit__property", "unit__property__landlord", "created_by"
        ).order_by("-created_at")

    @transaction.atomic
    def perform_create(self, serializer):
        lease = serializer.save(created_by=self.request.user)

        # LOCKING: Safe row locking to prevent status synchronization gaps
        if lease.status == Lease.LeaseStatus.ACTIVE:
            unit = Unit.objects.select_for_update().get(pk=lease.unit_id)
            unit.status = Unit.UnitStatus.OCCUPIED
            unit.save(update_fields=["status", "updated_at"])

    @transaction.atomic
    def perform_update(self, serializer):
        # Fetch unmodified information out of DB before transaction tracking updates it
        old_instance = self.get_object()
        old_unit_id = old_instance.unit_id
        old_status = old_instance.status

        lease = serializer.save()

        if lease.status == Lease.LeaseStatus.ACTIVE:
            new_unit = Unit.objects.select_for_update().get(pk=lease.unit_id)
            new_unit.status = Unit.UnitStatus.OCCUPIED
            new_unit.save(update_fields=["status", "updated_at"])

            # FIX: Cleans up the old unit status if the manager reassigns rooms mid-flight
            if old_unit_id != lease.unit_id:
                old_unit = Unit.objects.select_for_update().get(pk=old_unit_id)
                old_unit.status = Unit.UnitStatus.VACANT
                old_unit.save(update_fields=["status", "updated_at"])

        elif old_status == Lease.LeaseStatus.ACTIVE:
            old_unit = Unit.objects.select_for_update().get(pk=old_unit_id)
            old_unit.status = Unit.UnitStatus.VACANT
            old_unit.save(update_fields=["status", "updated_at"])

    @swagger_auto_schema(operation_summary="List leases", tags=["Leases"])
    def list(self, request, *args, **kwargs):
        self.check_dynamic_permission()
        response = super().list(request, *args, **kwargs)
        return api_response(True, "Leases fetched successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Retrieve lease", tags=["Leases"])
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()

        # KEPT: Your clean tenant-bypass implementation check
        if request.user.is_tenant and obj.tenant_id == request.user.id:
            response = super().retrieve(request, *args, **kwargs)
            return api_response(True, "Lease fetched successfully", response.data, status.HTTP_200_OK)

        self.check_dynamic_permission(property_id=obj.unit.property_id)
        response = super().retrieve(request, *args, **kwargs)
        return api_response(True, "Lease fetched successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create lease", request_body=LeaseSerializer, tags=["Leases"])
    def create(self, request, *args, **kwargs):
        unit_id = request.data.get("unit")

        if not unit_id:
            raise ValidationError({"unit": _("Unit is required to create a lease.")})

        try:
            unit = Unit.objects.select_related("property").get(id=unit_id, deleted_at__isnull=True)
        except Unit.DoesNotExist:
            raise ValidationError({"unit": _("Invalid or non-existent unit selection.")})

        self.check_dynamic_permission(property_id=unit.property_id)

        if not user_can_access_property_id(request.user, unit.property_id):
            raise PermissionDenied(_("You do not have access to this unit's property."))

        response = super().create(request, *args, **kwargs)
        return api_response(True, "Lease created successfully", response.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_summary="Update lease", request_body=LeaseSerializer, tags=["Leases"])
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_dynamic_permission(property_id=obj.unit.property_id)
        response = super().update(request, *args, **kwargs)
        return api_response(True, "Lease updated successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Partially update lease", request_body=LeaseSerializer, tags=["Leases"])
    def partial_update(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_dynamic_permission(property_id=obj.unit.property_id)
        response = super().partial_update(request, *args, **kwargs)
        return api_response(True, "Lease updated successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Soft delete lease", tags=["Leases"])
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_dynamic_permission(property_id=obj.unit.property_id)

        unit_id = obj.unit_id
        lease_status = obj.status

        obj.soft_delete()

        # LOCKING: Safe atomic cascade on soft deletions
        if lease_status == Lease.LeaseStatus.ACTIVE:
            unit = Unit.objects.select_for_update().get(pk=unit_id)
            unit.status = Unit.UnitStatus.VACANT
            unit.save(update_fields=["status", "updated_at"])

        return api_response(True, "Lease deleted successfully", None, status.HTTP_200_OK)
