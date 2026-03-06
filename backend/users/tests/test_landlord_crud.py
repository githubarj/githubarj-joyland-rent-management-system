import pytest
from django.urls import reverse
from users.models import TenantProfile
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def tenant_user2(db):
    user = User.objects.create_user(
        email="tenant2@example.com",
        password="pass1234",
        is_tenant=True,
    )
    # TenantProfile.objects.create(user=user)
    return user

@pytest.mark.django_db
def test_landlord_can_create_tenant(api_client, landlord_user, tenant_user2):
    api_client.force_authenticate(user=landlord_user)

    url = reverse("tenant-profiles-list")
    payload = {"user": tenant_user2.id, "national_id": "999999"}
    resp = api_client.post(url, payload)

    assert resp.status_code == 201, resp.json()
    assert resp.data["success"] is True

@pytest.mark.django_db
def test_landlord_can_update_tenant(api_client, landlord_user, tenant_user):
    api_client.force_authenticate(user=landlord_user)

    url = reverse("tenant-profiles-detail", args=[tenant_user.tenant_profile.id])
    payload = {"employer_name": "Airtel KE", "user":tenant_user.id}
    resp = api_client.patch(url, payload)

    assert resp.status_code == 200, resp.json()
    tenant_user.tenant_profile.refresh_from_db()
    assert tenant_user.tenant_profile.employer_name == "Airtel KE"

@pytest.mark.django_db
def test_landlord_can_soft_delete_tenant(api_client, landlord_user, tenant_user):
    api_client.force_authenticate(user=landlord_user)

    url = reverse("tenant-profiles-detail", args=[tenant_user.tenant_profile.id])
    resp = api_client.delete(url)

    assert resp.status_code == 200, resp.json()
    tenant_user.tenant_profile.refresh_from_db()
    assert tenant_user.tenant_profile.deleted_at is not None