from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ChangePasswordSerializer, RegisterSerializer, LoginSerializer, UserDetailSerializer
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.permissions import IsAuthenticatedAndActive


# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Register a new user and send email verification",
        request_body=RegisterSerializer,
        tags=['Auth'], 
        responses={
            201: openapi.Response(description="User registered successfully. Verification email sent"),
            400: openapi.Response(description="Validation failed or user already exists.")
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"},  status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
                        "access": "<ACCESS_TOKEN>",
                        "refresh": "<REFRESH_TOKEN>"
                    }
                }
            ),
            400: openapi.Response(description="Invalid credentials")
        }
    )
    def post(self, request,*args, **kwargs):
        # Validate credentials
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        })


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
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            return Response({"error": f"Token error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class UserMeView(APIView):
    
    permission_classes = [IsAuthenticatedAndActive]
    serializer_class = UserDetailSerializer

    @swagger_auto_schema(
        operation_summary="Get Authenticated User Details",
        operation_description="Returns authenticated user's details including roles.",
        responses={200: UserDetailSerializer()},
        security=[{"Bearer": []}]
    )

    def get(self, request):
        serializer =  UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticatedAndActive]
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(
        operation_summary="Change user password",
        request_body=ChangePasswordSerializer,
        responses={
            200: openapi.Response(description="Password changed successfully"),
            400: openapi.Response(description="Validation error"),
            401: openapi.Response(description="Authentication credentials were not provided"),
        },
        tags=['Auth'], 
    )
    def put(self, request):

        user = request.user
        serializer = ChangePasswordSerializer(data = request.data, context={'request':request})

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"error":"Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message":"Password changed Successfuly"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)