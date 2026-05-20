
from django.db import migrations

PROPERTY_PERMISSION_CODES = [
    ("can_view_properties", "Can view properties"),
    ("can_manage_properties", "Can create, update, and delete properties"),
    ("can_view_units", "Can view units"),
    ("can_manage_units", "Can create, update, and delete units"),
    ("can_view_leases", "Can view leases"),
    ("can_manage_leases", "Can create, update, and delete leases"),
]

def seed_permissions(apps, schema_editor):
    Permission = apps.get_model("users", "Permission")

    for code, description in PROPERTY_PERMISSION_CODES:
        Permission.objects.get_or_create(
            code=code,
            defaults={"description": description},
        )

def remove_permissions(apps, schema_editor):
    Permission = apps.get_model("users", "Permission")
    codes = [code for code, _ in PROPERTY_PERMISSION_CODES]
    Permission.objects.filter(code__in=codes).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
        ('users','0007_permission_managerprofile_landlordprofile_and_more')
    ]

    operations = [
        migrations.RunPython(seed_permissions, remove_permissions),
    ]
