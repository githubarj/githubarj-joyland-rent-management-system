from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import (PermissionSerializer, RolePermissionSerializer, UserPermissionSerializer)
from .models import  (Permission, RolePermission, UserPermission)
from drf_yasg.utils import swagger_auto_schema
from .permissions import IsAuthenticatedAndActive
from drf_yasg import openapi
from .utils import api_response


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(tags=["Permissions"],
        operation_summary="Get a permission",
        responses={
            200: openapi.Response(
                description="Permission fetched",
                examples={"application/json": {
                    "success": True, "message": "Permission fetched",
                    "data": {"id": 1, "code": "can_view_property", "description": "Can view properties"}
                }}
            ),
            404: openapi.Response(
                description="Not found",
                examples={"application/json": {"success": False, "message": "Permission not found", "data": None}}
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(True, "Permission fetched",serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Permissions"], 
        operation_summary="List permissions",
        responses={
        200: openapi.Response(
            description="List Permissions",
            examples={"application/json": {
                "success": True, "message": "Permissions fetched",
                "data": [{"id": 1, "code": "can_view_property", "description": "Can view properties"},
                         {"id": 2, "code": "can_edit_property", "description": "Can edit properties"}]
            }}
        ),
        401: openapi.Response(
                description="Unauthorized - user not authenticated",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(True,"Permissions fetched", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Permissions"], 
        operation_summary="Create permission", 
        request_body=PermissionSerializer,
        responses={
                201: openapi.Response(
                    description="Permission created successfully",
                    examples={
                        "application/json": {
                            "success": True,
                            "message": "Permission created",
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
                                "code": ["This field must be unique."]
                            }
                        }
                    }
                )
            }
        )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(True, "Permission created", response.data,status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=["Permissions"], 
        operation_summary="Update permission", 
        request_body=PermissionSerializer,
        responses={
            200: openapi.Response(
                description="Permission updated successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "User profile updated",
                        "data": {
                            "id": 1,
                            "code": "can_view_proprty 123",
                            "decsciption": "can view property 123",
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
                            "code": ["This field must be unique."]
                        }
                    }
                }
            ),
            404: openapi.Response(
                description="User not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Permission not found",
                        "data": None
                    }
                }
            ),
        }
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return api_response( True, "Permission updated", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Permissions"], 
        operation_summary="Delete permission",
        responses={
            200: openapi.Response(
                description="Permission deleted successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "User disabled",
                        "data": None
                    }
                }
            ),
            404: openapi.Response(
                description="Permission not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Permission not found",
                        "data": None
                    }
                }
            ),
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return api_response(True, "Permission deleted",  None, status.HTTP_200_OK)

class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Role Permissions"],
        operation_summary="Get a role permission mapping",
        responses={
            200: openapi.Response(
                description="Role permission fetched",
                examples={"application/json": {
                    "success": True, "message": "Role permission fetched",
                    "data": {"id": 1, "role": "property_manager", "permission": 5}
                }}
            ),
            404: openapi.Response(
                description="Not found",
                examples={"application/json": {"success": False, "message": "Role permission not found", "data": None}}
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(True, "Role permission fetched", serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Role Permissions"], 
        operation_summary="List role permissions",
        responses={
        200: openapi.Response(
            description="List Role Permission",
            examples={"application/json": {
                "success": True, "message": "Role Permission fetched",
                "data": [{"id": 1, "role": "accountant", "description": "Can view invoices"},
                         {"id": 2, "role": "viewer", "description": "Can view properties"}]
            }}
        ),
        401: openapi.Response(
                description="Unauthorized - user not authenticated",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(True, "Role permissions fetched", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Role Permissions"],
        operation_summary="Create role permission", 
        request_body=RolePermissionSerializer,
        responses={
                201: openapi.Response(
                    description="Role Permission created successfully",
                    examples={
                        "application/json": {
                            "success": True,
                            "message": "Role Permission created",
                            "data": {"role":"accountant", "permission":"can_manage_invoices"}
                        }
                    }
                ),
                400: openapi.Response(
                    description="Validation failed",
                    examples={
                        "application/json": {
                            "success": False,
                            "message": "Validation error",
                            "data": None
                        }
                    }
                )
            }
        )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(True, "Role permission created", response.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=["Role Permissions"], 
        operation_summary="Update role permission", 
        request_body=RolePermissionSerializer,
        responses={
            200: openapi.Response(
                description="Permission updated successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Role permssion profile updated",
                        "data": {
                            "id": 1,
                            "code": "can_view_proprty 123",
                            "decsciption": "can view property 123",
                        }
                    }
                }
            ),
            404: openapi.Response(
                description="Role Permission not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Role permission not found",
                        "data": None
                    }
                }
            ),
        }   
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return api_response( True,"Role permission updated", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Role Permissions"], 
        operation_summary="Delete role permission",
        responses={
            200: openapi.Response(
                description="Role permission deleted successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Role permission deleted",
                        "data": None
                    }
                }
            ),
            404: openapi.Response(
                description="Role permission not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Role permission not found",
                        "data": None
                    }
                }
            ),
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return api_response(True, "Role permission deleted", None, status.HTTP_200_OK)

class UserPermissionViewSet(viewsets.ModelViewSet):
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["User Permissions"],
        operation_summary="Get a user permission override",
        responses={
            200: openapi.Response(
                description="User permission fetched",
                examples={"application/json": {
                    "success": True, "message": "User permission fetched",
                    "data": {"id": 1, "user": 7, "permission": 5}  # add property if/when scoped
                }}
            ),
            404: openapi.Response(
                description="Not found",
                examples={"application/json": {"success": False, "message": "User permission not found", "data": None}}
            ),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(True,"User permission fetched",serializer.data, status.HTTP_200_OK)


    @swagger_auto_schema(tags=["User Permissions"], 
        operation_summary="List user permissions",
        responses={
        200: openapi.Response(
            description="List User Permission",
            examples={"application/json": {
                "success": True, "message": "User specific Permission fetched",
                "data": [{"id": 1, "user": "1", "description": "Can view invoices"},
                         {"id": 2, "role": "2", "description": "Can edit properties"}]
            }}
        ),
        401: openapi.Response(
                description="Unauthorized - user not authenticated",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return api_response(True, "User specific permissions fetched", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(tags=["User Permissions"], 
        operation_summary="Create user permission", 
        request_body=UserPermissionSerializer,
        responses={
            201: openapi.Response(
                description="User Permission created successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "User Permission created",
                        "data": {"user":"11", "permission":"5"}
                    }
                }
            ),
            400: openapi.Response(
                description="Validation failed",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Validation error",
                        "data": None
                    }
                }
            )
        }
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return api_response(True,"User permission created", response.data, status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=["User Permissions"], 
        operation_summary="Update user permission", 
        request_body=UserPermissionSerializer,
        responses={
            200: openapi.Response(
                description="Permission updated successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Role permssion profile updated",
                        "data": {
                            "id": 3,
                            "user": "3",
                            "permission": "5",
                        }
                    }
                }
            ),
            404: openapi.Response(
                description="User Permission not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "User permission not found",
                        "data": None
                    }
                }
            ),
        } 
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return api_response( True, "User permission updated", response.data, status.HTTP_200_OK)

    @swagger_auto_schema(tags=["User Permissions"], 
        operation_summary="Delete user permission",
        responses={
            200: openapi.Response(
                description="User permission deleted successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "User permission deleted",
                        "data": None
                    }
                }
            ),
            404: openapi.Response(
                description="User permission not found",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "User permission not found",
                        "data": None
                    }
                }
            )
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return api_response(True, "User permission deleted", None, status.HTTP_200_OK)
