from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Platform, PriceSnapshot, TrackedEvent
from .serializers import (
    EventSerializer,
    PlatformSerializer,
    PriceSnapshotSerializer,
    TrackedEventSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True, methods=["get"], url_path="price-history")
    def price_history(self, request, pk=None):
        event = self.get_object()
        snapshots = event.price_snapshots.all()
        serializer = PriceSnapshotSerializer(snapshots, many=True)
        return Response(serializer.data)


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class PriceSnapshotViewSet(viewsets.ModelViewSet):
    queryset = PriceSnapshot.objects.all()
    serializer_class = PriceSnapshotSerializer


class TrackedEventViewSet(viewsets.ModelViewSet):
    queryset = TrackedEvent.objects.all()
    serializer_class = TrackedEventSerializer