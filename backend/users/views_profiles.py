from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import (RegisterSerializer, UserSerializer, TenantProfileSerializer, ManagerProfileSerializer,
    LandlordProfileSerializer, LandlordPayoutMethodSerializer, PropertyManagerSerializer)
from .models import  (
    User, TenantProfile, ManagerProfile,
    LandlordProfile, LandlordPayoutMethod,
    PropertyManager)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .permissions import RBACPermission
from rest_framework.exceptions import PermissionDenied
from .utils import api_response

# ----------------- USERS -----------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, RBACPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_admin:
            return User.objects.all()
        return User.objects.none()


    @swagger_auto_schema(tags=["Users"],
        operation_summary="Get a user",
        responses={
            200: openapi.Response(
                description="User fetched",
                examples={"application/json": {
                    "success": True, "message": "User fetched",
                    "data": {
                        "id": 1, "email": "tenant@example.com",
                        "surname": "Doe", "other_names": "Jane",
                        "phone": "+254700000000",
                        "is_tenant": True, "is_manager": False
                    }
                }}
            ),
            404: openapi.Response(
                description="Not found",
                examples={"application/json": {"success": False, "message": "User not found", "data": None}}
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response( True, "User fetched", serializer.data, status.HTTP_200_OK)


    @swagger_auto_schema(tags=["Users"],
        operation_summary="List all users",
        responses={
            200: openapi.Response(
                description="List of all users",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Users fetched",
                        "data": [
                            {
                                "id": 1,
                                "email": "tenant@example.com",
                                "surname": "Doe",
                                "other_name": "Jane",
                                "phone": "+254700000000",
                                "roles": ["tenant"]
                            },
                            {
                                "id": 2,
                                "email": "manager@example.com",
                                "surname": "Smith",
                                "other_name": "John",
                                "phone": "+254711111111",
                                "roles": ["manager"]
                            }
                        ]
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized - user not authenticated",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            )
        }
    )
    def list(self, request, *args,**kwargs):
        response = super().list(request,*args, **kwargs)
        return api_response(True, "Users fetched",response.data,status.HTTP_200_OK)
    
    @swagger_auto_schema(tags=["Users"], 
            operation_summary="Create user",
            request_body=RegisterSerializer,
            responses={
                201: openapi.Response(
                    description="User created successfully",
                    examples={
                        "application/json": {
                            "success": True,
                            "message": "User created successfully",
                            "data": None
                        }
                    }
                ),
                400: openapi.Response(
                    description="Validation failed",
                    examples={
                        "application/json": {
                            "success": False,
                            "message": "Validation error",
                            "data": {
                                "email": ["This field must be unique."]
                            }
                        }
                    }
                )
            }
        )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(True,"User profile created",response.data,status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=["Users"],
        operation_summary="Update user profile",
        request_body=UserSerializer,  # 👈 expects UserSerializer fields
        responses={
            200: openapi.Response(
                description="User updated successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "User profile updated",
                        "data": {
                            "id": 1,
                            "email": "tenant@example.com",
                            "surname": "Doe",
                            "other_names": "Jane",
                            "phone": "+254700000000",
                            "roles": ["tenant"]
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Validation failed",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Validation error",
                        "data": {
                            "email": ["This field must be unique."]
                        }
                    }
                }
            ),
            404: openapi.Response(
                description="User not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "User not found",
                        "data": None
                    }
                }
            ),
        }
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return api_response(True, "User profile updated", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Users"],
        operation_summary="Disable user (soft delete)",
        responses={
            200: openapi.Response(
                description="User disabled successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "User disabled",
                        "data": None
                    }
                }
            ),
            404: openapi.Response(
                description="User not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "User not found",
                        "data": None
                    }
                }
            ),
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Object exists in queryset, so now apply action-level check
        if not request.user.is_superuser and not request.user.is_admin:
            raise PermissionDenied("Tenants cannot delete their own profile.")
        instance.soft_delete()   # call your custom soft delete
        return api_response(True, "User disabled", None,status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Users"],
        method="post",
        operation_summary="Restore a disabled (soft-deleted) user",
        responses={
            200: openapi.Response(
                description="User restored successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "User restored",
                        "data": {
                            "id": 1,
                            "email": "tenant@example.com",
                            "surname": "Doe",
                            "other_names": "Jane",
                            "phone": "+254700000000",
                            "roles": ["tenant"],
                            "is_active": True
                        }
                    }
                }
            ),
            404: openapi.Response(
                description="User not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "User not found",
                        "data": None
                    }
                }
            ),
        }
    )
    @action(detail=True, methods=["post"], url_path="restore")
    def restore_user(self, request, pk=None):
        """Restore a soft-deleted user"""
        try:
            instance = self.get_object()
            # Object exists in queryset, so now apply action-level check
            if not request.user.is_superuser and not request.user.is_admin:
                raise PermissionDenied("User cannot restore the profile.")
            instance.restore()
            serializer = self.get_serializer(instance)
            return api_response(
                True,"User restored", serializer.data,
                status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return api_response(
                 False, "User not found", None,
                status.HTTP_404_NOT_FOUND
            )

# ----------------- Tenants -----------------
class TenantProfileViewSet(viewsets.ModelViewSet):
    queryset = TenantProfile.objects.all()
    serializer_class = TenantProfileSerializer
    permission_classes = [IsAuthenticated, RBACPermission]
    required_permission = "can_manage_tenant_profiles"

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_admin:
            return TenantProfile.objects.all()
        if user.is_manager and hasattr(user, "landlord_profile"):
            return TenantProfile.objects.all()  # later: filter by landlord
        if user.is_tenant:
            return TenantProfile.objects.filter(user=user)
        return TenantProfile.objects.none()

    def get_required_permission(self):
        """Map actions to permission codes dynamically"""
        if self.action in ["list", "retrieve"]:
            return "can_view_tenant_profiles"
        if self.action in ["create", "update", "partial_update"]:
            return "can_manage_tenant_profiles"
        return None
    
    def get_permissions(self):
        # Attach required_permission so RBACPermission can check it
        self.required_permission = self.get_required_permission()
        return [permission() for permission in self.permission_classes]

    @swagger_auto_schema(tags=["Tenant Profiles"],
        operation_summary="Get a tenant profile",
        responses={
            200: openapi.Response(
                description="Tenant profile fetched",
                examples={"application/json": {
                    "success": True, "message": "Tenant profile fetched",
                    "data": {
                        "id": 1, "user": 5, "national_id": "12345678",
                        "employer_name": "Acme Corp",
                        "emergency_contact_name": "Jane Doe",
                        "emergency_contact_phone": "+254711111111"
                    }
                }}
            ),
            404: openapi.Response(
                description="Not found",
                examples={"application/json": {"success": False, "message": "Tenant profile not found", "data": None}}
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(True,"Tenant profile fetched",serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Tenant Profiles"], 
        operation_summary="List all tenant profiles",
        responses={
            200: openapi.Response(
                description="List of all tenants",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Tenants fetched",
                        "data": [
                            {
                                "id": 1,
                                "national_id": "7388874",
                                "employername": "Asila Asila",
                                "emergency_contact_name": "Jane",
                                "emergency_contact_phone": "+254700000000",
                                "user": ["id", "phone"]
                            },
                        ]
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized - user not authenticated",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            )
        }
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(True, "Tenant profiles fetched",response.data,status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Tenant Profiles"],
        operation_summary="Create tenant profile",
        request_body=TenantProfileSerializer,
        responses={
            201: openapi.Response(
                description="Tenant profile created successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Tenant profile created",
                        "data": {
                            "id": 1,
                            "user": 5,
                            "national_id": "12345678",
                            "employer_name": "Acme Corp",
                            "emergency_contact_name": "John Doe",
                            "emergency_contact_phone": "+254700000000"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Validation failed",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Validation error",
                        "data": {
                            "user": ["User must be a tenant to have TenantProfile"]
                        }
                    }
                }
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response( True,"Tenant profile created",response.data,status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=["Tenant Profiles"],
        operation_summary="Update tenant profile",
        request_body=TenantProfileSerializer,
        responses={
            200: openapi.Response(
                description="Tenant profile updated successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Tenant profile updated",
                        "data": {
                            "id": 1,
                            "user": 5,
                            "national_id": "12345678",
                            "employer_name": "Acme Corp",
                            "emergency_contact_name": "Jane Doe",
                            "emergency_contact_phone": "+254711111111"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Validation failed",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Validation error",
                        "data": {
                            "user": ["User must be a tenant to have TenantProfile"]
                        }
                    }
                }
            ),
            404: openapi.Response(
                description="Tenant profile not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Tenant profile not found",
                        "data": None
                    }
                }
            ),
        }
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return api_response(True, "Tenant profile updated", response.data,status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Tenant Profiles"],
        operation_summary="Delete tenant profile (soft delete)",
        responses={
            200: openapi.Response(
                description="Tenant profile deleted successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Tenant profile deleted",
                        "data": None
                    }
                }
            ),
            404: openapi.Response(
                description="Tenant profile not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Tenant profile not found",
                        "data": None
                    }
                }
            ),
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Object exists in queryset, so now apply action-level check
        if not request.user.is_superuser and not request.user.is_admin:
            if request.user.is_tenant and instance.user == request.user:
                raise PermissionDenied("Tenants cannot delete their own profile.")
        instance.soft_delete()   # ✅ calls model’s soft_delete instead of hard delete
        return api_response(True,"Tenant profile deleted", None, status.HTTP_200_OK)
    
    @swagger_auto_schema(tags=["Tenant Profiles"],
        method="post",
        operation_summary="Restore a deleted tenant profile",
        responses={
            200: openapi.Response(
                description="Tenant profile restored successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Tenant profile restored",
                        "data": {
                            "id": 1,
                            "user": 5,
                            "national_id": "12345678",
                            "employer_name": "Acme Corp",
                            "emergency_contact_name": "Jane Doe",
                            "emergency_contact_phone": "+254711111111"
                        }
                    }
                }
            ),
            404: openapi.Response(
                description="Tenant profile not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Tenant profile not found",
                        "data": None
                    }
                }
            ),
        }
    )
    @action(detail=True, methods=["post"], url_path="restore")
    def restore_profile(self, request, pk=None):
        """Restore a soft-deleted tenant profile"""

        try:
            instance = TenantProfile.all_objects.get(pk=pk)
            # Object exists in queryset, so now apply action-level check
            self.check_object_permissions(request, instance) 
            instance.restore()
            serializer = self.get_serializer(instance)
            return api_response(
                 True, "Tenant profile restored", serializer.data,
                status.HTTP_200_OK
            )
        except TenantProfile.DoesNotExist:
            return api_response(
                 False, "Tenant profile not found", None,status.HTTP_404_NOT_FOUND
            )
        

# ----------------- MANAGER PROFILES -----------------
class ManagerProfileViewSet(viewsets.ModelViewSet):
    queryset = ManagerProfile.objects.all()
    serializer_class = ManagerProfileSerializer
    permission_classes = [IsAuthenticated, RBACPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_admin:
            return ManagerProfile.objects.all()
        if user.is_manager and hasattr(user, "landlord_profile"):
            return ManagerProfile.objects.all()  # later: filter by landlord
        return ManagerProfile.objects.none()

    @swagger_auto_schema(tags=["Manager Profiles"], operation_summary="List all manager profiles")
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(True, "Manager profiles fetched",response.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Manager Profiles"],
        operation_summary="Get a manager profile",
        responses={
            200: openapi.Response(
                description="Manager profile fetched",
                examples={"application/json": {
                    "success": True, "message": "Manager profile fetched",
                    "data": {"id": 1, "user": 2, "role": "landlord"}
                }}
            ),
            404: openapi.Response(
                description="Not found",
                examples={"application/json": {"success": False, "message": "Manager profile not found", "data": None}}
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(True, "Manager profile fetched",serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Manager Profiles"],
        operation_summary="Create a manager profile",
        request_body=ManagerProfileSerializer,
        responses={
            201: openapi.Response(
                description="Manager profile created successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Manager profile created",
                        "data": {
                            "id": 1,
                            "user": 2,
                            "role": "landlord"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Validation failed",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Validation error",
                        "data": {"user": ["User must have is_manager=True"]}
                    }
                }
            )
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(True, "Manager profile created", response.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["Manager Profiles"],
        operation_summary="Update a manager profile",
        request_body=ManagerProfileSerializer,
        responses={
            200: openapi.Response(
                description="Manager profile updated",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Manager profile updated",
                        "data": {
                            "id": 1,
                            "user": 2,
                            "role": "accountant"
                        }
                    }
                }
            ),
            404: openapi.Response(
                description="Profile not found",
                examples={
                    "application/json": {"success": False, "message": "Manager profile not found", "data": None}
                }
            ),
        }
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return api_response(True, "Manager profile updated",response.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Manager Profiles"],
        operation_summary="Delete (soft delete) manager profile",
        responses={
            200: openapi.Response(
                description="Manager profile deleted",
                examples={"application/json": {"success": True, "message": "Manager profile deleted", "data": None}}
            ),
            404: openapi.Response(
                description="Not found",
                examples={"application/json": {"success": False, "message": "Manager profile not found", "data": None}}
            ),
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete() if hasattr(instance, "soft_delete") else instance.delete()
        return api_response(True,"Manager profile deleted",None, status.HTTP_200_OK)

class LandlordProfileViewSet(viewsets.ModelViewSet):
    queryset = LandlordProfile.objects.all()
    serializer_class = LandlordProfileSerializer
    permission_classes = [IsAuthenticated, RBACPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_admin:
            return LandlordProfile.objects.all()
        if user.is_manager and hasattr(user, "landlord_profile"):
            return LandlordProfile.objects.filter(user=user)  # later: filter by landlord
        return LandlordProfile.objects.none()

    @swagger_auto_schema(
        tags=["Landlord Profiles"],
        operation_summary="Get a landlord profile",
        responses={
            200: openapi.Response(
                description="Landlord profile fetched",
                examples={"application/json": {
                    "success": True, "message": "Landlord profile fetched",
                    "data": {"id": 1, "manager": 2, "company_name": "Acme Ltd", "kra_pin":"AD83475844","contact_phone":"0717357908"}
                }}
            ),
            404: openapi.Response(
                description="Not found",
                examples={"application/json": {"success": False, "message": "Landlord profile not found", "data": None}}
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(True, "Landlord profile fetched",serializer.data, status.HTTP_200_OK)


    @swagger_auto_schema(tags=["Landlord Profiles"], operation_summary="List all landlord profiles")
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(True, "Landlord profiles fetched", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Landlord Profiles"],
        operation_summary="Create a landlord profile",
        request_body=LandlordProfileSerializer,
        responses={
            201: openapi.Response(description="Landlord profile created", examples={
                "application/json": {"success": True, "message": "Landlord profile created", "data": {"id": 1, "manager": 2, "company_name":"xyz", "kra_pin":"AIEN3774546728", "contact_phone":"07845840302"}}
            }),
            400: openapi.Response(description="Validation error", examples={
                "application/json": {"success": False, "message": "Validation error", "data": {"manager": ["This field is required."]}}
            })
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(True,"Landlord profile created",response.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["Landlord Profiles"],
        operation_summary="Update landlord profile",
        request_body=LandlordProfileSerializer,
        responses={
            200: openapi.Response(description="Landlord profile updated", examples={
                "application/json": {"success": True, "message": "Landlord profile updated", "data": {"id": 1, "manager": 2, "company_name":"xyz", "kra_pin":"AIEN3774546728", "contact_phone":"07845840302"}}
            }),
            404: openapi.Response(description="Not found", examples={
                "application/json": {"success": False, "message": "Landlord profile not found", "data": None}
            })
        }
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return api_response(True,"Landlord profile updated",response.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Landlord Profiles"],
        operation_summary="Delete landlord profile (soft delete)",
        responses={
            200: openapi.Response(description="Landlord profile deleted", examples={
                "application/json": {"success": True, "message": "Landlord profile deleted", "data": None}
            }),
            404: openapi.Response(description="Not found", examples={
                "application/json": {"success": False, "message": "Landlord profile not found", "data": None}
            })
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Object exists in queryset, so now apply action-level check
        if not request.user.is_superuser and not request.user.is_admin:
            if request.user.is_manager and instance.user == request.user:
                raise PermissionDenied("Landlord cannot delete their own profile.")
        instance.soft_delete() if hasattr(instance, "soft_delete") else instance.delete()
        return api_response({"success": True, "message": "Landlord profile deleted", "data": None})
    
    @swagger_auto_schema(
        method="post",
        tags=["Landlord Profiles"],
        operation_summary="Restore a disabled (soft-deleted) Landlord",
        responses={
            200: openapi.Response(
                description="Landlord restored successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Landlord restored",
                        "data": {
                            "id": 1,
                            "is_active": True
                        }
                    }
                }
            ),
            404: openapi.Response(
                description="Landlord not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Landlord not found",
                        "data": None
                    }
                }
            ),
        }
    )
    @action(detail=True, methods=["post"], url_path="restore")
    def restore_user(self, request, pk=None):
        """Restore a soft-deleted user"""
        try:
            instance = self.get_object()
            # Object exists in queryset, so now apply action-level check
            if not request.user.is_superuser and not request.user.is_admin:
                if request.user.is_manager and instance.user == request.user:
                    raise PermissionDenied("Landlords cannot restore their own profile.")
            instance.restore()
            serializer = self.get_serializer(instance)
            return api_response(
                True,"Landlord restored", serializer.data,status.HTTP_200_OK
            )
        except LandlordProfile.DoesNotExist:
            return api_response(
                False, "Landlord not found", None,status.HTTP_404_NOT_FOUND
            )

class PropertyManagerViewSet(viewsets.ModelViewSet):
    queryset = PropertyManager.objects.all()
    serializer_class = PropertyManagerSerializer
    permission_classes = [IsAuthenticated, RBACPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_admin:
            return PropertyManager.objects.all()
        if user.is_manager and hasattr(user, "landlord_profile"):
            return PropertyManager.objects.all()  # later: filter by landlord
        if user.is_manager:
            return PropertyManager.objects.filter(user=user)
        return TenantProfile.objects.none()

    @swagger_auto_schema(
        tags=["Property Managers"],
        operation_summary="Get a property manager assignment",
        responses={
            200: openapi.Response(
                description="Property manager fetched",
                examples={"application/json": {
                    "success": True, "message": "Property manager fetched",
                    "data": {"id": 1, "user": 3, "role": "MANAGER"}
                }}
            ),
            404: openapi.Response(
                description="Not found",
                examples={"application/json": {"success": False, "message": "Property manager not found", "data": None}}
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(True, "Property manager fetched", serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Property Managers"], operation_summary="List property manager assignments")
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(True, "Property managers fetched",response.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Property Managers"],
        operation_summary="Assign a property manager",
        request_body=PropertyManagerSerializer,
        responses={
            201: openapi.Response(description="Assignment created", examples={
                "application/json": {"success": True, "message": "Property manager assigned", "data": {"id": 1, "user": 3, "role": "MANAGER", "invited_by":2}}
            })
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(True,"Property manager assigned", response.data,status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["Property Managers"],
        operation_summary="Update property manager assignment",
        request_body=PropertyManagerSerializer,
        responses={
            200: openapi.Response(description="Assignment updated", examples={
                "application/json": {"success": True, "message": "Property manager updated", "data": {"id": 1, "user": 3, "role": "ACCOUNTANT", "invited_by":2}}
            })
        }
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return api_response(True,"Property manager updated",response.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Property Managers"],
        operation_summary="Remove property manager (soft delete)",
        responses={
            200: openapi.Response(description="Assignment removed", examples={
                "application/json": {"success": True, "message": "Property manager removed", "data": None}
            })
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Object exists in queryset, so now apply action-level check
        if not request.user.is_superuser and not request.user.is_admin:
            if request.user.is_manager and instance.user == request.user:
                raise PermissionDenied("Property Managers cannot delete their own profile.")
        instance.soft_delete() if hasattr(instance, "soft_delete") else instance.delete()
        return api_response(True,"Property manager removed", None, status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Property Managers"],
        method="post",
        operation_summary="Restore a disabled (soft-deleted) Property Manager",
        responses={
            200: openapi.Response(
                description="Property Manager restored successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Property Manager restored",
                        "data": {
                            "id": 1,
                            "is_active": True
                        }
                    }
                }
            ),
            404: openapi.Response(
                description="User not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "User not found",
                        "data": None
                    }
                }
            ),
        }
    )
    @action(detail=True, methods=["post"], url_path="restore")
    def restore_user(self, request, pk=None):
        """Restore a soft-deleted user"""
        try:
            instance = self.get_object()
            if not request.user.is_superuser and not request.user.is_admin:
                if request.user.is_manager and instance.user == request.user:
                    raise PermissionDenied("Property Managers cannot restore their own profile.")
            instance.restore()
            serializer = self.get_serializer(instance)
            return api_response(True,"Property Manager restored", serializer.data,status.HTTP_200_OK)
        except PropertyManager.DoesNotExist:
            return api_response(False, "Property Manager not found", None,status.HTTP_404_NOT_FOUND)

# ----------------- LandLord Pay Methods -----------------
class LandlordPayoutMethodViewSet(viewsets.ModelViewSet):
    queryset = LandlordPayoutMethod.objects.all()
    serializer_class = LandlordPayoutMethodSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Landlord Payout Methods"],
        operation_summary="Get a payout method",
        responses={
            200: openapi.Response(
                description="Payout method fetched",
                examples={"application/json": {
                    "success": True, "message": "Payout method fetched",
                    "data": {"id": 1, "landlord": 2, "method": "BANK"}
                }}
            ),
            404: openapi.Response(
                description="Not found",
                examples={"application/json": {"success": False, "message": "Payout method not found", "data": None}}
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(True,"Payout method fetched", serializer.data, status.HTTP_200_OK)


    @swagger_auto_schema(tags=["Landlord Payout Methods"], operation_summary="List payout methods")
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(True, "Payout methods fetched",response.data,status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Landlord Payout Methods"],
        operation_summary="Create a payout method",
        request_body=LandlordPayoutMethodSerializer,
        responses={
            201: openapi.Response(description="Payout method created", examples={
                "application/json": {"success": True, "message": "Payout method created", "data": {"id": 1, "landlord": 2, "method": "BANK"}}
            })
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(True,"Payout method created",response.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(
        tags=["Landlord Payout Methods"],
        operation_summary="Update payout method",
        request_body=LandlordPayoutMethodSerializer,
        responses={
            200: openapi.Response(description="Payout method updated", examples={
                "application/json": {"success": True, "message": "Payout method updated", "data": {"id": 1, "landlord": 2, "method": "MPESA"}}
            })
        }
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return api_response(True,"Payout method updated", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Landlord Payout Methods"],
        operation_summary="Delete payout method",
        responses={
            200: openapi.Response(description="Payout method deleted", examples={
                "application/json": {"success": True, "message": "Payout method deleted", "data": None}
            })
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return api_response(True,"Payout method deleted", None, status.HTTP_200_OK)
    