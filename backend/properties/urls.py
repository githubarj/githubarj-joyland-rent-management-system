from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PropertyViewSet, UnitViewSet, LeaseViewSet

router = DefaultRouter()
router.register(r"properties", PropertyViewSet, basename="properties")
router.register(r"units", UnitViewSet, basename="units")
router.register(r"leases", LeaseViewSet, basename="leases")

urlpatterns = [
    path("", include(router.urls)),
]
