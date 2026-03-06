import pytest
from django.urls import reverse
from users.models import ManagerProfile, User


@pytest.fixture
def accountant_user(db):
    user = User.objects.create_user(
        email="accountant@example.com",
        password="pass1234",
        is_manager=True,
    )
    ManagerProfile.objects.create(user=user, role="accountant")
    return user


@pytest.mark.django_db
def test_accountant_cannot_create_tenant(api_client, accountant_user, tenant_user):
    api_client.force_authenticate(user=accountant_user)

    url = reverse("tenant-profiles-list")
    data = {"user": tenant_user.id, "national_id": "888888"}
    resp = api_client.post(url, data)

    assert resp.status_code == 403, resp.json()


@pytest.mark.django_db
def test_accountant_cannot_list_permissions(api_client, accountant_user):
    api_client.force_authenticate(user=accountant_user)

    url = reverse("permissions-list")
    resp = api_client.get(url)

    assert resp.status_code == 403, resp.json()
