from rest_framework import serializers

from .models import Property, Unit, Lease

class PropertySerializer(serializers.ModelSerializer):
    landlord_email = serializers.EmailField(source="landlord.email", read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "landlord",
            "landlord_email",
            "name",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "country",
            "postal_code",
            "notes",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]

    def validate_landlord(self, value):
        """
        A property must belong to a manager user.
        Later we can narrow this further to manager_profile.role == 'landlord'.
        """
        if not value.is_manager:
            raise serializers.ValidationError("Landlord must be a manager user.")

        return value

class UnitSerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source="property.name", read_only=True)

    class Meta:
        model = Unit
        fields = [
            "id",
            "property",
            "property_name",
            "unit_number",
            "unit_type",
            "bedrooms",
            "bathrooms",
            "floor",
            "base_rent",
            "deposit_required",
            "status",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]

    def validate(self, attrs):
        property_obj = attrs.get("property")
        unit_number = attrs.get("unit_number")

        # On update, use existing values if not provided
        if self.instance:
            property_obj = property_obj or self.instance.property
            unit_number = unit_number or self.instance.unit_number

        if property_obj and unit_number:
            duplicate_query = Unit.objects.filter(
                property = property_obj,
                unit_number__iexact = unit_number,
                deleted_at__isnull = True,
            )

            if self.instance:
                duplicate_query = duplicate_query.exclude(pk=slef.instance.pk)

            if duplicate_query.exists():
                raise serializers.ValidationError(
                    {
                        "unit_number": "A unit with this number already exists under this property."
                    }
                )

        return attrs

class LeaseSerializer(serializers.ModelSerializer):
    unit_number = serializers.CharField(source="unit.unit_number", read_only=True)
    property_name = serializers.CharField(source="unit.property.name", read_only=True)
    tenant_email = serializers.EmailField(source="tenant.email", read_only=True)

    rent_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
    )
    deposit_amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
    )

    class Meta:
        model = Lease
        fields = [
            "id",
            "unit",
            "unit_number",
            "property_name",
            "tenant",
            "tenant_email",
            "start_date",
            "end_date",
            "rent_amount",
            "deposit_amount",
            "billing_day",
            "status",
            "created_by",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at", "deleted_at"]

    def validate_tenant(self, value):
        if not value.is_tenant:
            raise serializers.ValidationError("Lease tenant must be a tenant user.")
        return value

    def validate_rent_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Rent amount cannot be negative.")
        return value

    def validate_deposit_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Deposit amount cannot be negative.")
        return value

    def validate_billing_day(self, value):
        if value < 1 or value > 28:
            raise serializers.ValidationError("Billing day must be between 1 and 28.")
        return value

    def validate(self, attrs):
        unit = attrs.get("unit")
        status = attrs.get("status")
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if self.instance:
            unit = unit or self.instance.unit
            status = status or self.instance.status
            start_date = start_date or self.instance.start_date
            end_date = end_date if "end_date" in attrs else self.instance.end_date

        if unit:
            attrs.setdefault("rent_amount", unit.base_rent)
            attrs.setdefault("deposit_amount", unit.deposit_required)

        if end_date and start_date and end_date < start_date:
            raise serializers.ValidationError(
                {"end_date": "End date cannot be before start date."}
            )

        if status == Lease.LeaseStatus.ACTIVE and unit:
            active_lease_query = Lease.objects.filter(
                unit=unit,
                status=Lease.LeaseStatus.ACTIVE,
                deleted_at__isnull=True,
            )

            if self.instance:
                active_lease_query = active_lease_query.exclude(pk=self.instance.pk)

            if active_lease_query.exists():
                raise serializers.ValidationError(
                    {"unit": "This unit already has an active lease."}
                )

        return attrs
