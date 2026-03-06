import pytest

from django.urls import reverse

@pytest.mark.django_db
def test_landlord_cannot_list_permissions(api_client, landlord_user):
    api_client.force_authenticate(user=landlord_user)

    url = reverse("permissions-list")
    response = api_client.get(url)

    assert response.status_code == 403

@pytest.mark.django_db
def test_admin_can_list_permissions(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)

    url = reverse("permissions-list")
    response = api_client.get(url)

    assert response.status_code == 200, response.json()
