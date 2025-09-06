from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "surname", "is_staff", "is_tenant", "is_manager", "email_verified_at", "date_joined", "updated_at", "deleted_at")
    list_filter = ("is_staff", "is_tenant", "is_manager")
    fieldsets = (
        (None, {"fields": ("email", "surname", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_tenant", "is_manager", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "surname","othernames", "phone", "password1", "password2", "is_tenant", "is_manager", "is_staff", "is_active")}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(User, CustomUserAdmin)
