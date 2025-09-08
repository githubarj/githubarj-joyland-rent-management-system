from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (ChangePasswordSerializer, RegisterSerializer, LoginSerializer, UserDetailSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer,
    UserSerializer, TenantProfileSerializer, ManagerProfileSerializer,
    LandlordProfileSerializer, LandlordPayoutMethodSerializer, PropertyManagerSerializer, PermissionSerializer, RolePermissionSerializer, UserPermissionSerializer)
from .models import  (
    User, TenantProfile, ManagerProfile,
    LandlordProfile, LandlordPayoutMethod,
    PropertyManager, Permission, RolePermission, UserPermission)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .permissions import IsAuthenticatedAndActive
from .utils import api_response

# ----------------- AUTH -----------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Register a new user and send email verification",
        request_body=RegisterSerializer,
        tags=['Auth'], 
        responses={
            201: openapi.Response(
                description="User registered successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "User registered successfully",
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
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(True, "User registered successfully", data=None, status=status.HTTP_201_CREATED )
        return api_response(False, "Validation error", data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    @swagger_auto_schema(
        operation_summary="Verify user email with token",
        tags=["Auth"],
        manual_parameters=[
            openapi.Parameter(
                'uidb64', openapi.IN_PATH, description="Base64 encoded user ID", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'token', openapi.IN_PATH, description="Token from verification email", type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: openapi.Response(description="Email verified successfully"),
            400: openapi.Response(description="Invalid token or user not found")
        }
    )
    def get(self, request, uidb64, token):
        try:
            uuid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uuid)

            if not default_token_generator.check_token(user, token):
                return api_response(False, "Invalid or expired token", None, status.HTTP_400_BAD_REQUEST)

            if not user.email_verified_at:
                user.email_verified_at = now()
                user.save()

            return api_response(True, "Email verified successfully", None, status.HTTP_200_OK)
        
        except Exception as e:
            return api_response(False, "Invalid or expired token", None, status.HTTP_400_BAD_REQUEST)

class ResendVerificationView(APIView):
    @swagger_auto_schema(
        operation_summary="Resend verification email",
        tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description="The email of the user to resend the verification link to")
            },
            required=['email']
        ),
        responses={
            200: "Verification email resent",
            400: "Invalid request or user already verified"
        }
    )
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            if user.email_verified_at:
                return Response({"message": "Email Account already verified."}, status=status.HTTP_400_BAD_REQUEST)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            verification_url = f"{settings.FRONTEND_BASE_URL}/verify-email/{uid}/{token}/"

            send_mail(
                subject="Resend: Verify your account",
                message=f"Click the link to verify your account: {verification_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
            )

            return Response({"message": "Verification email resent."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    serializer_classes = [PasswordResetSerializer]

    @swagger_auto_schema(
        operation_summary="Request a password reset email",
        tags=["Auth"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email"],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, format="email"),
            },
            example={  # 👈 One inline example
                "email": "user@example.com"
            }
        ),
        responses={
            200: openapi.Response(
                description="Reset email sent (generic success even if email not found)",
                examples={
                    "application/json": {"message": "Password reset link sent"}
                },
            ),
            400: openapi.Response(
                description="Validation error",
                examples={
                    "application/json": {"email": ["Enter a valid email address."]}
                },
            ),
        },
    )

    def post(self, request):
        serializer = PasswordResetSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(True, "Password Reset link sent",None, status=status.HTTP_200_OK)
        
        return api_response(True, f"Error: {serializer.errors}",None, status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    serializer_classes = [PasswordResetConfirmSerializer]

    @swagger_auto_schema(
        operation_summary="Reset password using uid/token",
        tags=["Auth"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["uid", "token", "new_password", "confirm_password"],
            properties={
                "uid": openapi.Schema(type=openapi.TYPE_STRING, description="Base64-encoded user ID (uidb64)"),
                "token": openapi.Schema(type=openapi.TYPE_STRING, description="Password reset token"),
                "new_password": openapi.Schema(type=openapi.TYPE_STRING, format="password"),
                "confirm_password": openapi.Schema(type=openapi.TYPE_STRING, format="password"),
            },
            example={  # 👈 Example payload shown in Swagger
                "uid": "MQ",  # Example uidb64 for user id 1
                "token": "5gq-0a2dcf7c9c9e1f0f0f6",  # Fake example token
                "new_password": "string",
                "confirm_password": "string"
            }
        ),
        responses={
            200: openapi.Response(
                description="Password reset successful",
                examples={"application/json": {"message": "Password reset successful"}}
            ),
            400: openapi.Response(
                description="Validation error",
                examples={
                    "application/json": {
                        "confirm_password": "Passwords do not match.",
                        "token": "Invalid or expired token.",
                        "new_password": ["This password is too short. It must contain at least 8 characters."]
                    }
                }
            ),
        },
    )

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(True,"Password reset successful",None,status.HTTP_200_OK)

        return api_response(False, f"Errors:{serializer.errors}", None, status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_summary="Login a user and return JWT tokens",
        request_body=LoginSerializer,
        tags=['Auth'], 
        responses={
            200: openapi.Response(
                description="JWT access and refresh tokens",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Login successful",
                        "data": {
                            "access": "<ACCESS_TOKEN>",
                            "refresh": "<REFRESH_TOKEN>",
                            "user": {
                                "id": 1,
                                "email": "tenant@example.com",
                                "surname": "Doe",
                                "other_name": "Jane",
                                "phone": "+254700000000",
                                "roles": ["tenant"]
                            }   
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid credentials",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Invalid email or password",
                        "data": None
                    }
                }
            ),
            403: openapi.Response(
                description="Email not verified",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Email not verified. Please verify your email first.",
                        "data": {
                            "code": "email_not_verified",
                            "email": "user@example.com",
                            "resend_endpoint": "/resend-verification/"
                        }
                    }
                }
            ),
            403: openapi.Response(
                description="User Inactive",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Your account is disabled. Please contact support.",
                        "data": {
                            "code": "account_disabled"
                        }
                    }
                }
            ),
            
        }
    )
    def post(self, request,*args, **kwargs):
        # Validate credentials
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if not user.email_verified_at:
            return api_response(False, 
                "Email not verified. Please verify your email first.", 
                {
                "code": "email_not_verified",
                "email": user.email,
                "resend_endpoint": "/resend-verification/"
                }, 
                status.HTTP_403_FORBIDDEN)
        
        # Respect admin suspensions
        if not user.is_active:
            return api_response(False, 
                    "Your account is disabled. Please contact support.", 
                    {
                    "code": "account_disabled"
                }, 
                status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)

        # ✅ Serialize user info
        user_data = UserDetailSerializer(user).data

        return api_response(True, "Login successful", {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": user_data
            }, status.HTTP_200_OK)

class LogoutView(APIView):
     
    @swagger_auto_schema(
        operation_summary="Logout user by blacklisting refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token to blacklist")
            }
        ),
        tags=['Auth'], 
        responses={
            205: openapi.Response(description="Logout successful"),
            400: openapi.Response(description="Token error or missing refresh token")
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return api_response(False, "Refresh token is required", None, status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return api_response(True, "Logout successful", None, status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            return api_response(False, f"Token error: {str(e)}", None, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return api_response(False, f"Error: {str(e)}", None, status.HTTP_400_BAD_REQUEST)

class UserMeView(APIView):
    
    permission_classes = [IsAuthenticatedAndActive]
    serializer_class = UserDetailSerializer

    @swagger_auto_schema(
        operation_summary="Get Authenticated User Details",
        operation_description="Returns authenticated user's details including roles.",
        responses={
            200: openapi.Response(
                description="User details",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "User details fetched successfully",
                        "data": {
                            "id": 1,
                            "email": "tenant@example.com",
                            "roles": ["tenant"]
                        }
                    }
                }
            )
        },
        security=[{"Bearer": []}]
    )

    def get(self, request):
        serializer =  UserDetailSerializer(request.user)
        return api_response(True, "User details fetched successfully", serializer.data, status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticatedAndActive]
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(
        operation_summary="Change user password",
        request_body=ChangePasswordSerializer,
        responses={
            200: openapi.Response(
                description="Password changed successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Password changed successfully",
                        "data": None
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Validation error",
                        "data": {"old_password": ["Old password is incorrect"]}
                    }
                }
            ),
            401: openapi.Response(
                description="Authentication required",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Authentication credentials were not provided.",
                        "data": None
                    }
                }
            ),
        },
        tags=['Auth'], 
    )
    def put(self, request):

        user = request.user
        serializer = ChangePasswordSerializer(data = request.data, context={'request':request})

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return api_response(False, "Old password is incorrect", None, status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return api_response(True, "Password changed successfully", None, status.HTTP_200_OK)

        return api_response(False, f"Error: {serializer.errors}", None, status.HTTP_400_BAD_REQUEST)

# ----------------- USERS -----------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Users"],
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

    @swagger_auto_schema(
        tags=["Users"],
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

    @swagger_auto_schema(
        tags=["Users"],
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
        instance.soft_delete()   # call your custom soft delete
        return api_response(True, "User disabled", None,status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        tags=["Users"],
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
            instance.restore()
            serializer = self.get_serializer(instance)
            return Response(
                {"success": True, "message": "User restored", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"success": False, "message": "User not found", "data": None},
                status=status.HTTP_404_NOT_FOUND
            )