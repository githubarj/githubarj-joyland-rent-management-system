from users.models import RolePermission, UserPermission, PropertyManager


def get_user_role(user):
    """
    Return the user's system role used for RolePermission checks.
    """
    if getattr(user, "is_tenant", False):
        return "tenant"

    if getattr(user, "is_manager", False) and hasattr(user, "manager_profile"):
        return user.manager_profile.role

    return None


def user_has_permission(user, permission_code, property_id=None):
    """
    Checks dynamic permissions from:
    1. Admin/superuser override
    2. RolePermission
    3. UserPermission global
    4. UserPermission scoped to a property
    """
    if not user or not user.is_authenticated:
        return False

    if user.is_superuser or getattr(user, "is_admin", False):
        return True

    role = get_user_role(user)

    has_role_permission = False
    if role:
        has_role_permission = RolePermission.objects.filter(
            role=role,
            permission__code=permission_code,
        ).exists()

    has_global_user_permission = UserPermission.objects.filter(
        user=user,
        permission__code=permission_code,
        property__isnull=True,
    ).exists()

    has_property_user_permission = False
    if property_id:
        has_property_user_permission = UserPermission.objects.filter(
            user=user,
            permission__code=permission_code,
            property_id=property_id,
        ).exists()

    return (
        has_role_permission
        or has_global_user_permission
        or has_property_user_permission
    )


def user_can_access_property(user, property_obj):
    """
    Checks if user has access to a specific property by ownership or assignment.
    This answers: "Can this user touch this property at all?"
    """
    if not user or not user.is_authenticated:
        return False

    if user.is_superuser or getattr(user, "is_admin", False):
        return True

    # Landlord owns the property
    if property_obj.landlord_id == user.id:
        return True

    # Property manager/accountant/viewer assigned to this property
    return PropertyManager.objects.filter(
        property=property_obj,
        user=user,
        is_active=True,
        deleted_at__isnull=True,
    ).exists()


def user_can_access_property_id(user, property_id):
    """
    Same as user_can_access_property, but accepts property_id.
    Useful during create requests where we only have IDs from request.data.
    """
    if not user or not user.is_authenticated:
        return False

    if user.is_superuser or getattr(user, "is_admin", False):
        return True

    from .models import Property

    try:
        property_obj = Property.objects.get(id=property_id, deleted_at__isnull=True)
    except Property.DoesNotExist:
        return False

    return user_can_access_property(user, property_obj)
