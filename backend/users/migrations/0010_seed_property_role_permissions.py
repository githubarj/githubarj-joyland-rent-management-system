from django.db import migrations

ROLE_PERMISSION_MAP = {
    "landlord": [
        "can_view_properties",
        "can_manage_properties",
        "can_view_units",
        "can_manage_units",
        "can_view_leases",
        "can_manage_leases",
    ],
    "property_manager": [
        "can_view_properties",
        "can_view_units",
        "can_manage_units",
        "can_view_leases",
    ],
    "accountant": [
        "can_view_properties",
        "can_view_units",
        "can_view_leases",
    ],
    "caretaker": [
        "can_view_properties",
        "can_view_units",
    ],
    "agent": [
        "can_view_properties",
        "can_view_units",
        "can_view_leases",
    ],
    "tenant": [
        "can_view_leases",
    ],
}


def seed_role_permissions(apps, schema_editor):
    Permission = apps.get_model("users", "Permission")
    RolePermission = apps.get_model("users", "RolePermission")

    for role, permission_codes in ROLE_PERMISSION_MAP.items():
        for code in permission_codes:
            permission = Permission.objects.filter(code=code).first()

            # DEBUG PRINT: This will print out to your docker logs so you can see if it's found
            if not permission:
                print(f"⚠️ WARNING: Permission code '{code}' was not found in the database!")
                continue

            RolePermission.objects.get_or_create(
                role=role,
                permission=permission,
            )

def remove_role_permissions(apps, schema_editor):
    Permission = apps.get_model("users", "Permission")
    RolePermission = apps.get_model("users", "RolePermission")

    all_codes = []
    for codes in ROLE_PERMISSION_MAP.values():
        all_codes.extend(codes)

    permissions = Permission.objects.filter(code__in=all_codes)

    RolePermission.objects.filter(
        role__in=ROLE_PERMISSION_MAP.keys(),
        permission__in=permissions,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        # Replace these with your actual latest migration names if different.
        ('users', '0009_seed_initial_permissions'),
        ('properties', '0002_seed_property_permissions'),
    ]

    operations = [
        migrations.RunPython(seed_role_permissions, remove_role_permissions),
    ]
