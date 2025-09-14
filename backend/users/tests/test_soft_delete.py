import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_soft_deleted_user_cannot_login(api_client, tenant_user):
    # Soft delete the user
    tenant_user.soft_delete()

    url = reverse("login")
    resp = api_client.post(url, {"email": tenant_user.email, "password": "pass1234"})

    assert resp.status_code in (400, 403), resp.json()
    assert resp.data["success"] is False

@pytest.mark.django_db
def test_soft_deleted_user_not_in_queryset(tenant_user):
    tenant_user.soft_delete()

    # Your UserManager excludes deleted_at != None  
    assert User.objects.filter(id=tenant_user.id).count() == 0

@pytest.mark.django_db
def test_admin_can_restore_soft_deleted_user(admin_user, tenant_user):
    tenant_user.soft_delete()
    assert not tenant_user.is_active

    tenant_user.restore()
    tenant_user.resresh_from_db()

    assert tenant_user.is_active is True
    assert tenant_user.is_deleted is None
