from decimal import Decimal
from random import randint, uniform
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.events.models import Event, Platform, PriceSnapshot

class Command(BaseCommand):
    help = "Seed sample events, platforms, and price snapshots"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        platforms = [
            ("Ticketmaster", "https://www.ticketmaster.com"),
            ("SeatGeek", "https://seatgeek.com"),
            ("StubHub", "https://www.stubhub.com"),
        ]

        platform_objects = []

        for name, website in platforms:
            platform, _ = Platform.objects.get_or_create(
                name=name,
                defaults={"website": website},
            )
            platform_objects.append(platform)
        
        events = [
            {
                "name": "Chicago Bulls vs Los Angeles Lakers",
                "category": Event.Category.SPORTS,
                "city": "Chicago",
                "venue": "United Center",
                "event_date": timezone.now() + timedelta(days=20),
            },
            {
                "name": "Taylor Swift Concert",
                "category": Event.Category.CONCERT,
                "city": "Chicago",
                "venue": "Soldier Field",
                "event_date": timezone.now() + timedelta(days=45),
            },
            {
                "name": "Chicago Cubs vs Milwaukee Brewers",
                "category": Event.Category.SPORTS,
                "city": "Chicago",
                "venue": "Wrigley Field",
                "event_date": timezone.now() + timedelta(days=10),
            },
        ]

        for event_data in events:
            event, _ = Event.objects.get_or_create(
                name=event_data["name"],
                city=event_data["city"],
                defaults=event_data,
            )

            for platform in platform_objects:
                base_price = randint(80, 250)

                for days_ago in range(14, -1, -1):
                    price = Decimal(str(round(base_price + uniform(-30, 30), 2)))

                    PriceSnapshot.objects.create(
                        event=event,
                        platform=platform,
                        lowest_price=price,
                        average_price=price + Decimal("25.00"),
                        currency="USD",
                        listing_count=randint(20, 300),
                        captured_at=timezone.now() - timedelta(days=days_ago),
                    )

        self.stdout.write(self.style.SUCCESS("Seed data created successfully."))


