from drf_yasg import openapi

# -----------------------------
# Common API envelope examples
# -----------------------------

def success_response(description, example_data=None, message="Success"):
    return openapi.Response(
        description=description,
        examples={
            "application/json": {
                "success": True,
                "message": message,
                "data": example_data,
            }
        },
    )


def error_response(description, message="Error", data=None):
    return openapi.Response(
        description=description,
        examples={
            "application/json": {
                "success": False,
                "message": message,
                "data": data,
            }
        },
    )


# -----------------------------
# Common error responses
# -----------------------------

COMMON_ERROR_RESPONSES = {
    400: error_response(
        "Validation error",
        message="Validation error",
        data={
            "field": ["Example validation error message."]
        },
    ),
    401: error_response(
        "Authentication required",
        message="Authentication credentials were not provided.",
        data={
            "detail": "Authentication credentials were not provided."
        },
    ),
    403: error_response(
        "Permission denied",
        message="You do not have permission to perform this action.",
        data={
            "detail": "You do not have permission to perform this action."
        },
    ),
    404: error_response(
        "Resource not found",
        message="Resource not found",
        data={
            "detail": "Not found."
        },
    ),
}


# -----------------------------
# Query parameters
# -----------------------------

PROPERTY_QUERY_PARAMS = [
    openapi.Parameter(
        "city",
        openapi.IN_QUERY,
        description="Filter properties by city.",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "is_active",
        openapi.IN_QUERY,
        description="Filter active/inactive properties. Use true/false.",
        type=openapi.TYPE_BOOLEAN,
    ),
    openapi.Parameter(
        "landlord",
        openapi.IN_QUERY,
        description="Filter properties by landlord user ID.",
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        "search",
        openapi.IN_QUERY,
        description="Search properties by name.",
        type=openapi.TYPE_STRING,
    ),
]

UNIT_QUERY_PARAMS = [
    openapi.Parameter(
        "property",
        openapi.IN_QUERY,
        description="Filter units by property ID.",
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        "status",
        openapi.IN_QUERY,
        description="Filter units by status. Example: VACANT, OCCUPIED, MAINTENANCE, RESERVED.",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "unit_type",
        openapi.IN_QUERY,
        description="Filter units by unit type. Example: ONE_BEDROOM, TWO_BEDROOM, COMMERCIAL.",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "is_active",
        openapi.IN_QUERY,
        description="Filter active/inactive units. Use true/false.",
        type=openapi.TYPE_BOOLEAN,
    ),
    openapi.Parameter(
        "search",
        openapi.IN_QUERY,
        description="Search units by unit number.",
        type=openapi.TYPE_STRING,
    ),
]

LEASE_QUERY_PARAMS = [
    openapi.Parameter(
        "tenant",
        openapi.IN_QUERY,
        description="Filter leases by tenant user ID.",
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        "unit",
        openapi.IN_QUERY,
        description="Filter leases by unit ID.",
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        "property",
        openapi.IN_QUERY,
        description="Filter leases by property ID.",
        type=openapi.TYPE_INTEGER,
    ),
    openapi.Parameter(
        "status",
        openapi.IN_QUERY,
        description="Filter leases by status. Example: PENDING, ACTIVE, TERMINATED, EXPIRED.",
        type=openapi.TYPE_STRING,
    ),
]


# -----------------------------
# Example data
# -----------------------------

PROPERTY_EXAMPLE = {
    "id": 1,
    "landlord": 2,
    "landlord_email": "landlord@example.com",
    "name": "Joyland Apartments",
    "address_line1": "Westlands Road",
    "address_line2": "Block A",
    "city": "Nairobi",
    "state": "Nairobi County",
    "country": "Kenya",
    "postal_code": "00100",
    "notes": "Main rental property",
    "is_active": True,
    "created_at": "2026-05-18T10:00:00Z",
    "updated_at": "2026-05-18T10:00:00Z",
    "deleted_at": None,
}

UNIT_EXAMPLE = {
    "id": 1,
    "property": 1,
    "property_name": "Joyland Apartments",
    "unit_number": "A1",
    "unit_type": "ONE_BEDROOM",
    "bedrooms": 1,
    "bathrooms": 1,
    "floor": "1",
    "base_rent": "25000.00",
    "deposit_required": "25000.00",
    "status": "VACANT",
    "is_active": True,
    "created_at": "2026-05-18T10:00:00Z",
    "updated_at": "2026-05-18T10:00:00Z",
    "deleted_at": None,
}

LEASE_EXAMPLE = {
    "id": 1,
    "unit": 1,
    "unit_number": "A1",
    "property_name": "Joyland Apartments",
    "tenant": 3,
    "tenant_email": "tenant@example.com",
    "start_date": "2026-05-01",
    "end_date": None,
    "rent_amount": "25000.00",
    "deposit_amount": "25000.00",
    "billing_day": 5,
    "status": "ACTIVE",
    "created_by": 2,
    "created_at": "2026-05-18T10:00:00Z",
    "updated_at": "2026-05-18T10:00:00Z",
    "deleted_at": None,
}
