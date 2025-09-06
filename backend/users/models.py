from datetime import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Custom manager to handle soft deletes and case-insensitive email lookup"""
    def get_queryset():
        # Exclude soft-deleted users by default
        return super().get_queryset().filter(deleted_at__isnull=True)
    
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


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    surname = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100, blank=True,null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Roles
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False, db_index=True)
    is_tenant = models.BooleanField(default=False, db_index=True)

    email_verified_at = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

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

    def soft_delete(self):
        """"Mark a user as deleted instead of removing from DB"""
        self.is_deleted_at = timezone.now()
        self.is_active = False
        self.save()
    
    def restore(self):
        """Restore a soft-deleted user"""
        self.is_deleted_at = None
        self.is_active = True
        self.save()

    def __str__(self):
        return f"self.email ({"Tenant" if self.is_tenant else "Manager" if self.is_manager else "User"})"

