from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings
from django.forms import ValidationError
from django.utils import timezone

User = settings.AUTH_USER_MODEL

ROLE_CHOICES = [
    ("landlord", "Landlord"),
    ("property_manager", "Property Manager"),
    ("accountant", "Accountant"),
    ("caretaker", "Caretaker"),
    ("agent", "Agent"),
    ("tenant", "Tenant"),  # ✅ added tenant role
]

class SoftDeleteManager(models.Manager):
    """Default manager excludes soft-deleted records"""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    """Abstract base class for soft delete functionality"""
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Managers
    objects = SoftDeleteManager()     # active only
    all_objects = models.Manager()    # everything (including soft deleted)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def restore(self):
        self.deleted_at = None
        self.is_active = True
        self.save()

    def delete(self, using=None, keep_parents=False):
        """Override delete() to always perform soft delete"""
        self.soft_delete()


class UserManager(BaseUserManager):
    """Custom manager to handle soft deletes and case-insensitive email lookup"""
    # def get_queryset(self):
    #     # Exclude soft-deleted users by default
    #     return super().get_queryset().filter(deleted_at__isnull=True)
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, SoftDeleteModel ):
    email = models.EmailField(unique=True)
    surname = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True,null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Roles
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False, db_index=True)
    is_tenant = models.BooleanField(default=False, db_index=True)

    email_verified_at = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["surname","phone"]

    objects = UserManager()

    class Meta:
        constraints = [
            #Ensure only one role active at a time (tenant or manager or neither)
            models.CheckConstraint(
                check =(
                    (models.Q(is_tenant=True, is_manager=False)) |
                    (models.Q(is_tenant=False, is_manager=True)) |
                    (models.Q(is_tenant=False, is_manager=False))
                ),
                name="users_one_role_ck"
            )
        ]
        indexes = [
            models.Index(fields=["is_tenant"], name="idx_users_is_tenant"),
            models.Index(fields=["is_manager"], name="idx_users_is_manager"),
            models.Index(fields=["email"], name="idx_users_email") #explicit email index
        ]

    @property
    def landlord_profile(self):
        if hasattr(self, "manager_profile"):
            return getattr(self.manager_profile, "landlord_profile", None)
        return None
    
    def __str__(self):
        role = "Tenant" if self.is_tenant else "Manager" if self.is_manager else "User"
        return f"{self.email} ({role})"

class ManagerProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="manager_profile")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.user.is_manager:
            raise ValidationError("User must have is_manager=True to create a ManagerProfile")
    
    def __str__(self):
        return f"{self.user.email} ({self.role})"

class TenantProfile(SoftDeleteModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="tenant_profile")
    national_id = models.CharField(max_length=100, blank=True, null=True)
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.user.is_tenant:
            raise ValidationError("User must have is_tenant=True to create a TenantProfile")
        
    def __str__(self):
        return f"TenantProfile for {self.user.email}"

class LandlordProfile(SoftDeleteModel):
    manager = models.OneToOneField(ManagerProfile, on_delete=models.CASCADE, related_name="landlord_profile")
    company_name = models.CharField(max_length=255, blank=True, null=True)
    kra_pin = models.CharField(max_length=50, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"LandlordProfile for {self.manager.user.email}"

class LandlordPayoutMethod(models.Model):
    METHOD_CHOICES = [
        ("BANK", "Bank"),
        ("MPESA", "M-PESA"),
        ("OTHER", "Other"),
    ]

    landlord = models.ForeignKey(LandlordProfile, on_delete=models.CASCADE, related_name="payout_methods")
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)

    # Bank fields
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    bank_account_name = models.CharField(max_length=255, blank=True, null=True)
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)

    # M-Pesa fields
    mpesa_paybill = models.CharField(max_length=50, blank=True, null=True)
    mpesa_till = models.CharField(max_length=50, blank=True, null=True)

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["landlord", "is_default"], condition=models.Q(is_default=True),
                                    name="unique_default_payout_per_landlord")
        ]

    def __str__(self):
        return f"{self.method} payout for {self.landlord.manager.user.email}"

class PropertyManager(SoftDeleteModel):
    ROLE_CHOICES = [
        ("MANAGER", "Manager"),
        ("ACCOUNTANT", "Accountant"),
        ("VIEWER", "Viewer"),
    ]
    # property = models.ForeignKey("properties.Property", on_delete=models.CASCADE, related_name="managers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="managed_properties")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    invited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="invitations_sent")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        # constraints = [
        #     models.UniqueConstraint(fields=["property", "user"], name="unique_property_user")
        # ]
        indexes = [
            models.Index(fields=["user"], name="idx_property_manager_user")
        ]
    
    def __str__(self):
        return f"{self.user.email} ({self.role})"
        # return f"{self.user.email} ({self.role}) for {self.property}"

class Permission(models.Model):
    """Atomic capability, e.g. 'can_view_users', 'can_manage_invoices'"""
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class RolePermission(models.Model):
    """Default permissions granted to roles (from ManagerProfile.role)""" 
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="role_assignements")

    class Meta:
        unique_together = ("role", "permission")

    def __str__(self):
        return f"{self.role} → {self.permission.code}"

class UserPermission(models.Model):
    """Overrides at user level (can be global or property-scoped)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="custom_permissions")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="user_assignment")
    # property = models.ForeignKey("properties.Property", null=True, blank=True,
    #                              on_delete=models.CASCADE, related_name="user_permissions")
    
    # class Meta:
    #     unique_together = ("user", "permission", "property")
    
    def __str__(self):
        # scope = f" for {self.property}" if self.property else " (global)"
        # return f"{self.user.email} → {self.permission.code}{scope}" 
        return f"{self.user.email} → {self.permission.code}" 

    
