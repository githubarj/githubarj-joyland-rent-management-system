import pytest
from django.contrib.auth import get_user_model
from users.models import TenantProfile, ManagerProfile, LandlordProfile

User = get_user_model()

import pytest
import os

# Create or clear the isolated failure log file at the start of the session
@pytest.fixture(scope="session", autouse=True)
def clean_failure_log():
    log_path = "/app/test_failures.log"
    if os.path.exists(log_path):
        os.remove(log_path)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute the test step to get the outcome report
    outcome = yield
    report = outcome.get_result()

    # ONLY catch when a test actually crashes during execution
    if report.when == "call" and report.failed:
        with open("/app/test_failures.log", "a") as f:
            f.write("=" * 80 + "\n")
            f.write(f"❌ FAILED TEST: {item.nodeid}\n")
            f.write("=" * 80 + "\n")

            # Extract and log only the exact exception traceback text
            if report.longrepr:
                f.write(str(report.longrepr))
            f.write("\n\n")


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
