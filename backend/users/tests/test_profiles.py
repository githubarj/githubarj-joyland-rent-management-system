import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import TenantProfile, ManagerProfile, LandlordProfile

User = get_user_model()

@pytest.mark.django_db
def test_user_cannot_have_two_profile(api_client, admin_user, tenant_user):
    api_client.force_authenticate(user=admin_user)

    url = reverse("users-detail", args=[tenant_user.id])
    payload = {"is_manager": True}
    response = api_client.patch(url, payload)

    assert response.status_code == 400

@pytest.mark.django_db
def test_tenant_can_view_own_profile(api_client, tenant_user):
    api_client.force_authenticate(user=tenant_user)
    url = reverse("tenant-profiles-detail", args=[tenant_user.tenant_profile.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["data"]["id"] == tenant_user.tenant_profile.id

@pytest.mark.django_db
def test_tenant_cannot_view_other_profiles(api_client, tenant_user, landlord_user):

    # Arrange: create another tenant
    other = User.objects.create_user(email="other@example.com", password="pass1234", is_tenant=True)
    TenantProfile.objects.create(user=other)

    api_client.force_authenticate(user=tenant_user)
    
    url= reverse("tenant-profiles-detail", args=[landlord_user.manager_profile.id]) #wrong-profile
    response = api_client.get(url) 

    # should not expose other tenant/manager profiles
    assert response.status_code in (404, 403)

@pytest.mark.django_db
def test_tenant_cannot_create_profile(api_client, tenant_user):
    api_client.force_authenticate(user=tenant_user)

    url = reverse("tenant-profiles-list")
    data = {"user": tenant_user.id, "national_id": "12345678"}
    response = api_client.post(url, data)

    assert response.status_code == 403

