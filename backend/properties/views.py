from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from .models import Property, Unit, Lease
from .serializers import PropertySerializer, UnitSerializer, LeaseSerializer
from users.permissions import IsAuthenticatedAndActive
from users.utils import api_response

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_queryset(self):
        # FIX: Added missing '=True' to the isnull lookup
        # OPTIMIZATION: Moved select_related here to group DB setup together
        queryset = Property.objects.filter(deleted_at__isnull=True).select_related("landlord")

        params = self.request.query_params
        city = params.get("city")
        is_active = params.get("is_active")
        landlord = params.get("landlord")
        search = params.get("search")

        if city:
            queryset = queryset.filter(city__icontains=city)

        if is_active is not None:
            # FIX: Explicitly checks for true strings to prevent false-negative filtering
            queryset = queryset.filter(is_active=is_active.lower() in ["true", "1"])

        if landlord:
            # VALIDATION: Prevents database ValueError crashes from malformed strings
            if not landlord.isdigit():
                raise ValidationError({"landlord": _("Invalid landlord ID format.")})
            queryset = queryset.filter(landlord_id=landlord)

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset.order_by("-created_at")

    @swagger_auto_schema(
        operation_summary="List properties",
        tags=["Properties"],
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(
            True,
            "Properties fetched successfully",
            response.data,
            status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary="Create property",
        request_body=PropertySerializer,
        tags=["Properties"],
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(
            True,
            "Property created successfully",
            response.data,
            status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(
        operation_summary="Retrieve property",
        tags=["Properties"],
    )
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return api_response(
            True,
            "Property fetched successfully",
            response.data,
            status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary="Update property",
        request_body=PropertySerializer,
        tags=["Properties"],
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return api_response(
            True,
            "Property updated successfully",
            response.data,
            status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary="Partially update property",
        request_body=PropertySerializer,
        tags=["Properties"],
    )
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return api_response(
            True,
            "Property updated successfully",
            response.data,
            status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary="Soft delete property",
        tags=["Properties"],
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()

        return api_response(
            True,
            "Property deleted successfully",
            None,
            status.HTTP_200_OK,
        )


from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError

# Define custom API responses or mixins if you wish to eliminate repeated boilerplate method overrides completely.

class UnitViewSet(viewsets.ModelViewSet):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_queryset(self):
        queryset = Unit.objects.filter(deleted_at__isnull=True).select_related(
            "property", "property__landlord"
        )

        params = self.request.query_params
        property_id = params.get("property")
        status_param = params.get("status")
        unit_type = params.get("unit_type")
        is_active = params.get("is_active")
        search = params.get("search")

        if property_id:
            if not property_id.isdigit():
                raise ValidationError({"property": _("Invalid property ID format.")})
            queryset = queryset.filter(property_id=property_id)

        if status_param:
            queryset = queryset.filter(status=status_param)

        if unit_type:
            queryset = queryset.filter(unit_type=unit_type)

        if is_active is not None:
            # FIX: Properly parse parameters to avoid filtering everything out when None
            queryset = queryset.filter(is_active=is_active.lower() in ["true", "1"])

        if search:
            queryset = queryset.filter(unit_number__icontains=search)

        return queryset.order_by("property_id", "unit_number")

    @swagger_auto_schema(operation_summary="List units", tags=["Units"])
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(True, "Units fetched successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create unit", request_body=UnitSerializer, tags=["Units"])
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(True, "Unit created successfully", response.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_summary="Retrieve unit", tags=["Units"])
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return api_response(True, "Unit fetched successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update unit", request_body=UnitSerializer, tags=["Units"])
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return api_response(True, "Unit updated successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Partially update unit", request_body=UnitSerializer, tags=["Units"])
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return api_response(True, "Unit updated successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Soft delete unit", tags=["Units"])
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return api_response(True, "Unit deleted successfully", None, status.HTTP_200_OK)


class LeaseViewSet(viewsets.ModelViewSet):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_queryset(self):
        queryset = Lease.objects.filter(deleted_at__isnull=True).select_related(
            "tenant", "unit", "unit__property", "unit__property__landlord", "created_by"
        )

        params = self.request.query_params
        tenant = params.get("tenant")
        unit = params.get("unit")
        property_id = params.get("property")
        status_param = params.get("status")

        if tenant:
            if not tenant.isdigit():
                raise ValidationError({"tenant": _("Invalid tenant ID format.")})
            queryset = queryset.filter(tenant_id=tenant)

        if unit:
            if not unit.isdigit():
                raise ValidationError({"unit": _("Invalid unit ID format.")})
            queryset = queryset.filter(unit_id=unit)

        if property_id:
            if not property_id.isdigit():
                raise ValidationError({"property": _("Invalid property ID format.")})
            queryset = queryset.filter(unit__property_id=property_id)

        if status_param:
            queryset = queryset.filter(status=status_param)

        return queryset.order_by("-created_at")

    @transaction.atomic
    def perform_create(self, serializer):
        lease = serializer.save(created_by=self.request.user)

        # LOCKING: Lock the unit record to safely guarantee status synchronization
        if lease.status == Lease.LeaseStatus.ACTIVE:
            unit = Unit.objects.select_for_update().get(pk=lease.unit_id)
            unit.status = Unit.UnitStatus.OCCUPIED
            unit.save(update_fields=["status", "updated_at"])

    @transaction.atomic
    def perform_update(self, serializer):
        # Obtain unmodified data prior to serialization commits
        old_instance = self.get_object()
        old_unit_id = old_instance.unit_id
        old_status = old_instance.status

        lease = serializer.save()

        # FIX: Resolve unit state transitions safely across transactions
        if lease.status == Lease.LeaseStatus.ACTIVE:
            # Case A: Lease continues/becomes active on a fresh or modified unit assignment
            new_unit = Unit.objects.select_for_update().get(pk=lease.unit_id)
            new_unit.status = Unit.UnitStatus.OCCUPIED
            new_unit.save(update_fields=["status", "updated_at"])

            # Case B: Lease changed its unit registration mid-flight; free up the abandoned unit
            if old_unit_id != lease.unit_id:
                old_unit = Unit.objects.select_for_update().get(pk=old_unit_id)
                old_unit.status = Unit.UnitStatus.VACANT
                old_unit.save(update_fields=["status", "updated_at"])

        # Case C: Lease changed status from ACTIVE to anything else (TERMINATED/EXPIRED)
        elif old_status == Lease.LeaseStatus.ACTIVE:
            old_unit = Unit.objects.select_for_update().get(pk=old_unit_id)
            old_unit.status = Unit.UnitStatus.VACANT
            old_unit.save(update_fields=["status", "updated_at"])

    @swagger_auto_schema(operation_summary="List leases", tags=["Leases"])
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(True, "Leases fetched successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create lease", request_body=LeaseSerializer, tags=["Leases"])
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(True, "Lease created successfully", response.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_summary="Retrieve lease", tags=["Leases"])
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return api_response(True, "Lease fetched successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update lease", request_body=LeaseSerializer, tags=["Leases"])
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return api_response(True, "Lease updated successfully", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Partially update lease", request_body=LeaseSerializer, tags=["Leases"])
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return api_response(True, "Lease updated successfully", response.data, status.HTTP_200_OK)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        unit_id = instance.unit_id
        lease_status = instance.status

        instance.soft_delete()

        # LOCKING: Lock record on cascading soft deletions
        if lease_status == Lease.LeaseStatus.ACTIVE:
            unit = Unit.objects.select_for_update().get(pk=unit_id)
            unit.status = Unit.UnitStatus.VACANT
            unit.save(update_fields=["status", "updated_at"])

        return api_response(True, "Lease deleted successfully", None, status.HTTP_200_OK)
