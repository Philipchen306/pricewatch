from django.contrib import admin
from .models import Event, Platform, PriceSnapshot, TrackedEvent


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "category",
        "city",
        "venue",
        "event_date",
        "created_at",
    ]
    list_filter = ["category", "city", "event_date"]
    search_fields = ["name", "city", "venue", "external_id"]


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "website", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(PriceSnapshot)
class PriceSnapshotAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "event",
        "platform",
        "lowest_price",
        "average_price",
        "currency",
        "listing_count",
        "captured_at",
    ]
    list_filter = ["platform", "currency", "captured_at"]
    search_fields = ["event__name", "platform__name"]


@admin.register(TrackedEvent)
class TrackedEventAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "event",
        "target_price",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "created_at"]
    search_fields = ["email", "event__name"]