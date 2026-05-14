from django.db import models
from django.db.models import Q

from django.utils import timezone

from django.conf import settings


# Create your models here.

class Property(models.Model):
    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.PROTECT,
        related_name = "properties",
    )

    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default="Kenya")
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["landlord"], name="idx_property_landlord"),
            models.Index(fields=["city"], name="idx_property_city"),
            models.Index(fields=["is_active"], name="idx_property_is_active"),
        ]

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save(update_fields=["deleted_at", "is_active", "updated_at"])

    def __str__(self):
        return self.name

class Unit(models.Model):
    class UnitType(models.TextChoices):
        SINGLE_ROOM = "SINGLE_ROOM", "Single Room"
        BEDSITTER = "BEDSITTER", "Bedsitter"
        ONE_BEDROOM = "ONE_BEDROOM", "One Bedroom"
        TWO_BEDROOM = "TWO_BEDROOM", "Two Bedroom"
        THREE_BEDROOM = "THREE_BEDROOM", "Three Bedroom"
        COMMERCIAL = "COMMERCIAL", "Commercial"
        OTHER = "OTHER", "Other"

    class UnitStatus(models.TextChoices):
        VACANT = "VACANT", "Vacant"
        OCCUPIED = "OCCUPIED", "Occupied"
        MAINTENANCE = "MAINTENANCE", "Maintenance"
        RESERVED = "RESERVED", "Reserved"

    property = models.ForeignKey(
        Property,
        on_delete = models.CASCADE,
        related_name = "units",
    )

    unit_number = models.CharField(max_length=50)
    unit_type = models.CharField(
        max_length=30,
        choices = UnitType.choices,
        default = UnitType.OTHER,
    )

    bedrooms = models.PositiveSmallIntegerField(blank=True, null=True)
    bathrooms = models.PositiveSmallIntegerField(blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)

    base_rent = models.DecimalField(max_digits=12, decimal_places = 2)
    deposit_required = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status =  status = models.CharField(
        max_length=30,
        choices=UnitStatus.choices,
        default=UnitStatus.VACANT,
        db_index=True,
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["property", "unit_number"],
                condition=Q(deleted_at__isnull=True),
                name="uniq_active_unit_number_per_property",
            )
        ]
        indexes = [
            models.Index(fields=["property"], name="idx_unit_property"),
            models.Index(fields=["status"], name="idx_unit_status"),
            models.Index(fields=["is_active"], name="idx_unit_is_active"),
        ]

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save(update_fields=["deleted_at", "is_active", "updated_at"])

    def __str__(self):
        return f"{self.property.name} - {self.unit_number}"

class Lease(models.Model):
    class LeaseStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        TERMINATED = "TERMINATED", "Terminated"
        EXPIRED = "EXPIRED", "Expired"

    unit = models.ForeignKey(
        Unit,
        on_delete = models.PROTECT,
        related_name = "leases",
    )

    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="leases",
    )

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    rent_amount = models.DecimalField(max_digits=12, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    billing_day = models.PositiveSmallIntegerField(default=1)

    status = models.CharField(
        max_length = 30,
        choices = LeaseStatus.choices,
        default=LeaseStatus.PENDING,
        db_index=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_leases",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(billing_day__gte=1) & Q(billing_day__lte=28),
                name="lease_billing_day_1_28_ck",
            ),
            models.CheckConstraint(
                check=Q(end_date__isnull=True) | Q(end_date__gte=models.F("start_date")),
                name="lease_end_date_after_start_date_ck",
            ),
            models.UniqueConstraint(
                fields=["unit"],
                condition=Q(status="ACTIVE", deleted_at__isnull=True),
                name="uniq_active_lease_per_unit",
            ),
        ]
        indexes = [
            models.Index(fields=["tenant"], name="idx_lease_tenant"),
            models.Index(fields=["unit"], name="idx_lease_unit"),
            models.Index(fields=["status"], name="idx_lease_status"),
            models.Index(fields=["start_date"], name="idx_lease_start_date"),
        ]

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"])

    def __str__(self):
        return f"{self.tenant} - {self.unit} ({self.status})"
