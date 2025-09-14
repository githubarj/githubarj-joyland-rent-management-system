import pytest
from django.contrib.auth import get_user_model
from users.models import TenantProfile, ManagerProfile, LandlordProfile

User = get_user_model()

import pytest
from django.contrib.auth import get_user_model
from users.models import TenantProfile, ManagerProfile, LandlordProfile

User = get_user_model()

@pytest.fixture
def admin_user(db):
    # This will have is_staff=True and is_superuser=True
    return User.objects.create_superuser(
        email="admin@example.com",
        password="pass1234",
    )

@pytest.fixture
def landlord_user(db):
    user = User.objects.create_user(
        email="landlord@example.com",
        password="pass1234",
        is_manager=True,
    )
    manager_profile = ManagerProfile.objects.create(user=user, role="landlord")
    LandlordProfile.objects.create(manager=manager_profile)
    return user

@pytest.fixture
def tenant_user(db):
    user = User.objects.create_user(
        email="tenant@example.com",
        password="pass1234",
        is_tenant=True,
    )
    TenantProfile.objects.create(user=user)
    return user

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
