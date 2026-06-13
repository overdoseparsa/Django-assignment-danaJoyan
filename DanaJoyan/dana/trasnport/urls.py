from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .routers import CompanyViewSet

router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")

urlpatterns = [
    path("", include(router.urls)),
]
