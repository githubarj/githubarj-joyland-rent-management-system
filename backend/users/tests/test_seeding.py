import pytest
from users.models import Permission, RolePermission


@pytest.mark.django_db
def test_permissions_seeded(db):
    codes = set(Permission.objects.values_list("code", flat=True))
    # check some expected codes
    assert "can_view_tenant_profiles" in codes
    assert "can_manage_tenant_profiles" in codes


@pytest.mark.django_db
def test_role_permissions_seeded(db):
    landlord_codes = set(
        RolePermission.objects.filter(role="landlord")
        .values_list("permission__code", flat=True)
    )
    assert "can_manage_tenant_profiles" in landlord_codes
