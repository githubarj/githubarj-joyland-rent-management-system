from django.conf import settings
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Must be at least 8 characters and not entirely numeric.",
    )
    class Meta:
        model = User
        fields = ("email","full_name", "password", "is_tenant", "is_landlord")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  # ✅ Hash the password
        user.is_active = False # ✅ Inactivates the user until email verification
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        verification_url = f"{settings.FRONTEND_BASE_URL}/verify-email/{uid}/{token}/"

        send_mail(
            subject="Verify your account",
            message=f"Click the link to verify your account: {verification_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )

        return user   

         
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Enter your email")
    password = serializers.CharField(write_only=True, help_text="Must be 8+ characters")

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        data['user'] = user
        return data
    
class UserDetailSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'roles', 'date_joined', 'is_active']
    
    def get_roles(self, obj):
        roles = []
        if obj.is_admin:
            roles.append("admin")
        if obj.is_tenant:
            roles.append("tenant")
        if obj.is_landlord:
            roles.append("landlord")
        return roles

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Must be at least 8 characters and not entirely numeric."
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Re-enter the new password for confirmation."
    )

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, data):
        if data.get("new_password") != data.get("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data