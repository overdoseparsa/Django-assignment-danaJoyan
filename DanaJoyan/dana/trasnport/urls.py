from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .routers import BusApiviewset, CompanyViewSet, SeatApiviewset, TransportApiview

router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"buses", BusApiviewset, basename="bus")
router.register(r"seats", SeatApiviewset, basename="seat")


urlpatterns = [
    path("", include(router.urls)),
    path("transport/", TransportApiview.as_view(), name="transport"),
]
