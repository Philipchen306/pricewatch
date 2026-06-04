from rest_framework.routers import DefaultRouter
from .views import (
    EventViewSet,
    PlatformViewSet,
    PriceSnapshotViewSet,
    TrackedEventViewSet,
)

router = DefaultRouter()

router.register("events", EventViewSet)
router.register("platforms", PlatformViewSet)
router.register("price-snapshots", PriceSnapshotViewSet)
router.register("tracked-events", TrackedEventViewSet)

urlpatterns = router.urls