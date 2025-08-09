from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("email", "full_name", "is_staff", "is_tenant", "is_landlord", "email_verified_at", "date_joined", "updated_at")
    list_filter = ("is_staff", "is_tenant", "is_landlord")
    fieldsets = (
        (None, {"fields": ("email", "full_name", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_tenant", "is_landlord", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2", "is_tenant", "is_landlord", "is_staff", "is_active")}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(User, CustomUserAdmin)
