from django.urls import include, path
from rest_framework import DefaultRouter

from .views import PropertyViewSet, UnitViewSet, LeaseViewSet

router = DefaultRouter()
router.register(r"properties", PropertyViewSet, basename="properties")
router.register(r"units", UnitViewSet, basename="properties")
router.register(r"leases", LeaseViewSet, basename="properties")

urlpatterns = [
    path("", include(router.urls)),
]
