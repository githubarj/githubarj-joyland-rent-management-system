from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.timezone import now
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
                return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.is_active:
                return Response({"message": "Account already verified"}, status=status.HTTP_200_OK)
            
            user.is_active = True
            user.email_verified_at = now()
            user.save()

            return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
            if user.is_active:
                return Response({"message": "Account already verified."}, status=status.HTTP_400_BAD_REQUEST)

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