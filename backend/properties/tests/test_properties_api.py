import pytest
from rest_framework.test import APIClient

from users.models import (
    User,
    Permission,
    RolePermission,
    ManagerProfile,
    TenantProfile,
    PropertyManager,
)
from properties.models import Property, Unit, Lease

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def landlord_user(db):
    user = User.objects.create_user(
        email="landlord@example.com",
        password="StrongPass123!",
        surname="Landlord",
        other_name="User",
        is_manager=True,
        is_tenant=False,
        email_verified_at="2026-01-01T00:00:00Z",
    )

    ManagerProfile.objects.create(
        user=user,
        role="landlord",
    )

    return user

@pytest.fixture
def property_manager_user(db):
    user = User.objects.create_user(
        email="manager@example.com",
        password="StrongPass123!",
        surname="Manager",
        other_name="User",
        is_manager=True,
        is_tenant=False,
        email_verified_at="2026-01-01T00:00:00Z",
    )

    ManagerProfile.objects.create(
        user=user,
        role="property_manager",
    )

    return user

@pytest.fixture
def tenant_user(db):
    user = User.objects.create_user(
        email="tenant@example.com",
        password="StrongPass123!",
        surname="Tenant",
        other_name="User",
        is_tenant=True,
        is_manager=False,
        email_verified_at="2026-01-01T00:00:00Z",
    )

    TenantProfile.objects.create(
        user=user,
        national_id="12345678",
    )

    return user

@pytest.fixture
def second_tenant_user(db):
    user = User.objects.create_user(
        email="tenant2@example.com",
        password="StrongPass123!",
        surname="TenantTwo",
        other_name="User",
        is_tenant=True,
        is_manager=False,
        email_verified_at="2026-01-01T00:00:00Z",
    )

    TenantProfile.objects.create(
        user=user,
        national_id="87654321",
    )

    return user

@pytest.fixture
def seed_permissions(db):
    permission_codes = [
        "can_view_properties",
        "can_manage_properties",
        "can_view_units",
        "can_manage_units",
        "can_view_leases",
        "can_manage_leases",
    ]

    permissions = {}

    for code in permission_codes:
        permission, _ = Permission.objects.get_or_create(
            code=code,
            defaults={"description": code.replace("_", " ").title()},
        )
        permissions[code] = permission

    landlord_permissions = [
        "can_view_properties",
        "can_manage_properties",
        "can_view_units",
        "can_manage_units",
        "can_view_leases",
        "can_manage_leases",
    ]

    for code in landlord_permissions:
        RolePermission.objects.get_or_create(
            role="landlord",
            permission=permissions[code],
        )

    property_manager_permissions = [
        "can_view_properties",
        "can_view_units",
        "can_manage_units",
        "can_view_leases",
    ]

    for code in property_manager_permissions:
        RolePermission.objects.get_or_create(
            role="property_manager",
            permission=permissions[code],
        )

    RolePermission.objects.get_or_create(
        role="tenant",
        permission=permissions["can_view_leases"],
    )

    return permissions

@pytest.fixture
def property_obj(db, landlord_user):
    return Property.objects.create(
        landlord=landlord_user,
        name="Joyland Apartments",
        address_line1="Westlands Road",
        city="Nairobi",
        country="Kenya",
    )


@pytest.fixture
def unit_obj(db, property_obj):
    return Unit.objects.create(
        property=property_obj,
        unit_number="A1",
        unit_type=Unit.UnitType.ONE_BEDROOM,
        bedrooms=1,
        bathrooms=1,
        floor="1",
        base_rent="25000.00",
        deposit_required="25000.00",
        status=Unit.UnitStatus.VACANT,
    )


@pytest.fixture
def active_lease(db, unit_obj, tenant_user, landlord_user):
    lease = Lease.objects.create(
        unit=unit_obj,
        tenant=tenant_user,
        start_date="2026-05-01",
        rent_amount="25000.00",
        deposit_amount="25000.00",
        billing_day=5,
        status=Lease.LeaseStatus.ACTIVE,
        created_by=landlord_user,
    )

    unit_obj.status = Unit.UnitStatus.OCCUPIED
    unit_obj.save(update_fields=["status"])

    return lease


#Tests from here

@pytest.mark.django_db
def test_landlord_can_create_property(api_client, landlord_user, seed_permissions):
    api_client.force_authenticate(user=landlord_user)

    payload = {
        "landlord": landlord_user.id,
        "name": "Green Heights",
        "address_line1": "Kilimani Road",
        "address_line2": "",
        "city": "Nairobi",
        "state": "Nairobi County",
        "country": "Kenya",
        "postal_code": "00100",
        "notes": "Test property",
    }

    response = api_client.post("/api/properties/", payload, format="json")

    assert response.status_code == 201
    assert response.data["success"] is True
    assert response.data["message"] == "Property created successfully"
    assert Property.objects.filter(name="Green Heights").exists()
