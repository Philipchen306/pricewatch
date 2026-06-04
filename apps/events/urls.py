from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    EventViewSet,
    PlatformViewSet,
    PriceSnapshotViewSet,
    TrackedEventViewSet,

    TicketmasterSearchView
)

router = DefaultRouter()

router.register("events", EventViewSet)
router.register("platforms", PlatformViewSet)
router.register("price-snapshots", PriceSnapshotViewSet)
router.register("tracked-events", TrackedEventViewSet)

urlpatterns = router.urls + [
    path("ticketmaster/search/", TicketmasterSearchView.as_view()),
]