from django.conf import settings
from .models import User, TenantProfile, ManagerProfile,LandlordProfile, LandlordPayoutMethod,PropertyManager, Permission, RolePermission, UserPermission
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import force_bytes
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()
# ----------------- Auth -----------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Must be at least 8 characters and not entirely numeric.",
    )
    class Meta:
        model = User
        fields = ("email", "password","surname","other_names","phone", "is_tenant", "is_manager")
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

        user.email_verified_at = None
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
        fields = ['id', 
            'email', 
            'roles',
            'surname',
            'other_names',
            'phone',
            'date_joined', 
            'is_active']
    
    def get_roles(self, obj):
        roles = []
        if obj.is_admin:
            roles.append("Admin")
        if obj.is_tenant:
            roles.append("Tenant")
        if obj.is_manager:
            roles.append("Manager")
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

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value
    
    def save(self):
        email = self.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"{settings.FRONTEND_BASE_URL}/reset-password-confirm/{uid}/{token}"

        send_mail(
            subject="Reset your password",
            message=f"Click to reset your password: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list = [email],
            fail_silently=False
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(help_text="Base64 user id from the email link")
    token = serializers.CharField(help_text="Password reset token from the email link")
    new_password = serializers.CharField(write_only=True, help_text="New password")
    confirm_password = serializers.CharField(write_only=True, help_text="Repeat new password")

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        
        #Decode user
        try:
            uid = urlsafe_base64_decode(attrs["uid"]).decode()
            user = User.objects.get(pk=uid)
        except:
            raise serializers.ValidationError({"uid": "Invalid user identifier."})
        
        #Validate_token

        if not default_token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError({"token":"Invalid or expired token"})
        
        # Password validators
        try:
            validate_password(attrs["new_password"], user=user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        # Stash user for save()
        self.user = user
        return attrs
    
    def save(self, **kwargs):
        self.user.set_password(self.validated_data["new_password"])
        self.user.save()
        return self.user

# ----------------- USERS -----------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = fields = (
            "id", "email", "surname", "other_names", "phone",
            "is_tenant", "is_manager", "is_active",
            "email_verified_at", "date_joined", "updated_at"
        )

# ----------------- TENANT PROFILES -----------------
class TenantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantProfile
        fields = "__all__"

    def validate(self, attrs):
        user = attrs.get("user")
        if user is None:
            raise serializers.ValidationError({"user": "This field is required."})
        if not getattr(user, "is_tenant", False):
            raise serializers.ValidationError({"user": "User must be a tenant to have TenantProfile."})
        return attrs
        
# ----------------- MANAGER PROFILES -----------------
class ManagerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerProfile
        fields = "__all__"
    
    def validate(self, attrs):
        """
        Ensures only users with is_manager=True can have a ManagerProfile.
        """
        user = attrs.get("user")

        if user is None:
            # raise, don't return a ValidationError
            raise serializers.ValidationError({"user": "This field is required."})

        # If 'user' is a pk (rare with ModelSerializer, but safe to handle)
        if not isinstance(user, User):
            try:
                user = User.objects.get(pk=user)
                attrs["user"] = user
            except User.DoesNotExist:
                raise serializers.ValidationError({"user": "User does not exist."})

        if not getattr(user, "is_manager", False):
            raise serializers.ValidationError({"user": "User must have is_manager=True to create a ManagerProfile."})

        return attrs  # ← IMPORTANT

class LandlordProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordProfile
        fields = "__all__"

class LandlordPayoutMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandlordPayoutMethod
        fields = "__all__"

class PropertyManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyManager
        fields = "__all__"

# ----------------- PERMISSIONS -----------------
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = "__all__"
    
class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = "__all__"

