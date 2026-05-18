from django.contrib import admin

from .models import Property, Unit, Lease

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "landlord",
        "city",
        "is_active",
        "created_at",
        "deleted_at",
    )
    list_filter = ("is_active", "city", "country", "created_at")
    search_fields = (
        "name",
        "landlord__email",
        "address_line1",
        "city",
    )
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    ordering = ("-created_at",)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "unit_number",
        "property",
        "unit_type",
        "status",
        "base_rent",
        "deposit_required",
        "is_active",
    )
    list_filter = ("status", "unit_type", "is_active", "created_at")
    search_fields = (
        "unit_number",
        "property__name",
        "property__landlord__email",
    )
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    ordering = ("property", "unit_number")


@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "unit",
        "status",
        "start_date",
        "end_date",
        "rent_amount",
        "billing_day",
        "created_at",
    )
    list_filter = ("status", "billing_day", "start_date", "created_at")
    search_fields = (
        "tenant__email",
        "unit__unit_number",
        "unit__property__name",
    )
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    ordering = ("-created_at",)
