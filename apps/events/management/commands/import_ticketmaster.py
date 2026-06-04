from django.core.management.base import BaseCommand
from django.db import transaction

from apps.events.models import Event, Platform, PriceSnapshot
from apps.scrapers.ticketmaster import search_ticketmaster_events


class Command(BaseCommand):
    help = "Import events and price data from Ticketmaster"

    def add_arguments(self, parser):
        parser.add_argument("--keyword", type=str, default="Chicago Bulls")
        parser.add_argument("--city", type=str, default="Chicago")
        parser.add_argument("--size", type=int, default=10)

    @transaction.atomic
    def handle(self, *args, **options):
        keyword = options["keyword"]
        city = options["city"]
        size = options["size"]

        self.stdout.write(f"Searching Ticketmaster: keyword={keyword}, city={city}")

        platform, _ = Platform.objects.get_or_create(
            name="Ticketmaster",
            defaults={
                "website": "https://www.ticketmaster.com",
                "is_active": True,
            },
        )

        events = search_ticketmaster_events(
            keyword=keyword,
            city=city,
            size=size,
        )

        created_events = 0
        created_snapshots = 0

        for item in events:
            if not item["external_id"] or not item["event_date"]:
                continue

            event, created = Event.objects.update_or_create(
                external_id=item["external_id"],
                defaults={
                    "name": item["name"],
                    "category": Event.Category.SPORTS,
                    "city": item["city"] or city,
                    "venue": item["venue"],
                    "event_date": item["event_date"],
                    "source_url": item["source_url"],
                },
            )

            if created:
                created_events += 1

            if item["lowest_price"] is not None:
                PriceSnapshot.objects.create(
                    event=event,
                    platform=platform,
                    lowest_price=item["lowest_price"],
                    average_price=item["highest_price"],
                    currency=item["currency"],
                    listing_count=0,
                )
                created_snapshots += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(events)} Ticketmaster events. "
                f"Created events: {created_events}. "
                f"Created price snapshots: {created_snapshots}."
            )
        )