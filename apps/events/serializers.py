from rest_framework import serializers
from .models import Event, Platform, PriceSnapshot, TrackedEvent


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = "__all__"


class PriceSnapshotSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source="event.name", read_only=True)
    platform_name = serializers.CharField(source="platform.name", read_only=True)

    class Meta:
        model = PriceSnapshot
        fields = "__all__"


class TrackedEventSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source="event.name", read_only=True)

    class Meta:
        model = TrackedEvent
        fields = "__all__"