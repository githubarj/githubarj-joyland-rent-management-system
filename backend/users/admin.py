# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    Permission, ManagerProfile, LandlordProfile, TenantProfile,
    UserPermission, LandlordPayoutMethod, PropertyManager, RolePermission
)

User = get_user_model()

# ---------- Utilities: Soft-delete admin mixin & filters ----------
class SoftDeletedFilter(admin.SimpleListFilter):
    title = "deleted status"
    parameter_name = "deleted"

    def lookups(self, request, model_admin):
        return (
            ("no", "Active (not deleted)"),
            ("yes", "Soft-deleted"),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == "no":
            return queryset.filter(deleted_at__isnull=True)
        if val == "yes":
            return queryset.filter(deleted_at__isnull=False)
        return queryset


class SoftDeleteAdminMixin:
    """Use all_objects in admin so staff can see soft-deleted rows; add actions."""
    actions = ("soft_delete_selected", "restore_selected")

    def get_queryset(self, request):
        # If model has all_objects, use it; else fallback to default
        qs = super().get_queryset(request)
        if hasattr(self.model, "all_objects"):
            return self.model.all_objects.all()
        return qs

    @admin.action(description="Soft delete selected")
    def soft_delete_selected(self, request, queryset):
        count = 0
        for obj in queryset:
            if hasattr(obj, "soft_delete"):
                obj.soft_delete()
                count += 1
        self.message_user(request, f"Soft-deleted {count} object(s).")

    @admin.action(description="Restore selected")
    def restore_selected(self, request, queryset):
        count = 0
        for obj in queryset:
            if hasattr(obj, "restore"):
                obj.restore()
                count += 1
        self.message_user(request, f"Restored {count} object(s).")


# ---------- User ----------
@admin.register(User)
class UserAdmin(SoftDeleteAdminMixin, BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "surname", "other_names", "phone",
                    "is_active", "is_manager", "is_tenant", "deleted_at")
    list_filter = ("is_active", "is_manager", "is_tenant", SoftDeletedFilter)
    search_fields = ("email", "surname", "other_names", "phone")
    readonly_fields = ("date_joined", "last_login", "updated_at", "deleted_at")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("surname", "other_names", "phone")}),
        (_("Roles"), {"fields": ("is_admin", "is_manager", "is_tenant")}),
        (_("Status"), {"fields": ("is_active", "deleted_at")}),
        (_("Permissions"), {"fields": ("is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "updated_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("surname", "other_names", "phone","email", "password1", "password2"),
        }),
    )


# ---------- ManagerProfile ----------
@admin.register(ManagerProfile)
class ManagerProfileAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("id", "user_email", "role", "created_at", "updated_at")
    list_filter = ("role",)
    search_fields = ("user__email",)
    autocomplete_fields = ("user",)
    ordering = ("-created_at",)

    def user_email(self, obj):
        return getattr(obj.user, "email", "")
    user_email.short_description = "User Email"


# ---------- LandlordPayoutMethod Inline ----------
class LandlordPayoutMethodInline(admin.TabularInline):
    model = LandlordPayoutMethod
    extra = 0
    fields = ("method", "bank_name", "bank_account_name", "bank_account_number",
              "mpesa_paybill", "mpesa_till", "is_default")
    show_change_link = True


# ---------- LandlordProfile ----------
@admin.register(LandlordProfile)
class LandlordProfileAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("id", "manager_email", "company_name", "kra_pin",
                    "contact_phone", "created_at", "updated_at")
    list_filter = (SoftDeletedFilter,)
    search_fields = ("manager__user__email", "company_name", "kra_pin")
    inlines = [LandlordPayoutMethodInline]
    autocomplete_fields = ("manager",)
    ordering = ("-created_at",)

    def manager_email(self, obj):
        return getattr(getattr(obj.manager, "user", None), "email", "")
    manager_email.short_description = "Manager Email"


# ---------- TenantProfile ----------
@admin.register(TenantProfile)
class TenantProfileAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("id", "user_email", "national_id",
                    "employer_name", "created_at", "updated_at", "deleted_at")
    list_filter = (SoftDeletedFilter,)
    search_fields = ("user__email", "national_id", "employer_name")
    autocomplete_fields = ("user",)
    ordering = ("-created_at",)

    def user_email(self, obj):
        return getattr(obj.user, "email", "")
    user_email.short_description = "User Email"


# ---------- PropertyManager ----------
@admin.register(PropertyManager)
class PropertyManagerAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("id", "user_email", "role", "invited_by_email",
                    "is_active", "created_at", "updated_at", "deleted_at")
    list_filter = ("role", "is_active", SoftDeletedFilter)
    search_fields = ("user__email", "invited_by__email")
    autocomplete_fields = ("user", "invited_by")
    ordering = ("-created_at",)

    def user_email(self, obj):
        return getattr(obj.user, "email", "")
    def invited_by_email(self, obj):
        return getattr(obj.invited_by, "email", "")
    user_email.short_description = "User Email"
    invited_by_email.short_description = "Invited By"


# ---------- LandlordPayoutMethod ----------
@admin.register(LandlordPayoutMethod)
class LandlordPayoutMethodAdmin(admin.ModelAdmin):
    list_display = ("id", "landlord_id", "method", "is_default", "created_at", "updated_at")
    list_filter = ("method", "is_default")
    search_fields = ("landlord__manager__user__email",)
    autocomplete_fields = ("landlord",)
    ordering = ("-created_at",)

    def landlord_id(self, obj):
        return getattr(obj.landlord, "id", None)


# ---------- Permission / RolePermission / UserPermission ----------
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("code", "description")
    search_fields = ("code", "description")
    ordering = ("code",)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "role", "permission_code")
    list_filter = ("role",)
    search_fields = ("role", "permission__code")
    autocomplete_fields = ("permission",)
    ordering = ("role", "permission__code")

    def permission_code(self, obj):
        return getattr(obj.permission, "code", "")
    permission_code.short_description = "Permission"


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "user_email", "permission_code")
    search_fields = ("user__email", "permission__code")
    autocomplete_fields = ("user", "permission")
    ordering = ("user__email", "permission__code")

    def user_email(self, obj):
        return getattr(obj.user, "email", "")
    def permission_code(self, obj):
        return getattr(obj.permission, "code", "")
    user_email.short_description = "User Email"
    permission_code.short_description = "Permission"
