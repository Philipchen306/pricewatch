from django.db.models import Avg, Min, Max, Count

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
from apps.scrapers.mock import fetch_mock_price

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True, methods=["get"], url_path="price-history")
    def price_history(self, request, pk=None):
        event = self.get_object()
        snapshots = event.price_snapshots.all()
        serializer = PriceSnapshotSerializer(snapshots, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="lowest-price")
    def lowest_price(self, request, pk=None):
        event = self.get_object()

        lowest_snapshot = (
            event.price_snapshots
            .order_by("lowest_price")
            .first()
        )

        if not lowest_snapshot:
            return Response(
                {"error": "No price data found"},
                status=404
            )

        return Response({
            "event": event.name,
            "platform": lowest_snapshot.platform.name,
            "lowest_price": lowest_snapshot.lowest_price,
            "currency": lowest_snapshot.currency,
            "captured_at": lowest_snapshot.captured_at,
        })

    @action(detail=True, methods=["get"], url_path="price-summary")
    def price_summary(self, request, pk=None):
        event = self.get_object()

        summary = event.price_snapshots.aggregate(
            min_price=Min("lowest_price"),
            max_price=Max("lowest_price"),
            average_price=Avg("lowest_price"),
            snapshot_count=Count("id"),
        )

        platform_count = (
            event.price_snapshots
            .values("platform")
            .distinct()
            .count()
        )

        if summary["snapshot_count"] == 0:
            return Response(
                {"error": "No price data found for this event"},
                status=404,
            )

        return Response({
            "event_id": event.id,
            "event": event.name,
            "city": event.city,
            "venue": event.venue,
            "event_date": event.event_date,
            "lowest_price": summary["min_price"],
            "highest_price": summary["max_price"],
            "average_price": round(summary["average_price"], 2),
            "platform_count": platform_count,
            "snapshot_count": summary["snapshot_count"],
        })
    @action(detail=True, methods=["get"], url_path="refresh-price")
    def refresh_price(self, request, pk=None):
        event = self.get_object()

        platforms = Platform.objects.filter(is_active=True)

        if not platforms.exists():
            return Response(
                {"error": "No active platforms found"},
                status=404
            )

        created_snapshots = []

        for platform in platforms:
            price_data = fetch_mock_price(event, platform)

            snapshot = PriceSnapshot.objects.create(**price_data)
            created_snapshots.append(snapshot)

        serializer = PriceSnapshotSerializer(created_snapshots, many=True)

        return Response({
            "message": "Price refreshed successfully",
            "event": event.name,
            "created_count": len(created_snapshots),
            "snapshots": serializer.data,
        })


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


class PriceSnapshotViewSet(viewsets.ModelViewSet):
    queryset = PriceSnapshot.objects.all()
    serializer_class = PriceSnapshotSerializer


class TrackedEventViewSet(viewsets.ModelViewSet):
    queryset = TrackedEvent.objects.all()
    serializer_class = TrackedEventSerializer