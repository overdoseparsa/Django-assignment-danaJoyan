from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .routers import BusApiviewset, CompanyViewSet

router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"buses", BusApiviewset, basename="bus")
urlpatterns = [
    path("", include(router.urls)),
]
