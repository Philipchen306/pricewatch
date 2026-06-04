from django.db import models

class Event(models.Model):
    class Category(models.TextChoices):
        SPORTS = "sports", "Sports"
        CONCERT = "concert", "Concert"
        FLIGHT = "flight", "Flight"
        OTHER = "other", "Other"

    name = models.CharField(max_length=255)
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        default=Category.SPORTS,
    )
    city = models.CharField(max_length=100)
    venue = models.CharField(max_length=255, blank=True)
    event_date = models.DateTimeField()

    source_url = models.URLField(blank=True)
    external_id = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["event_date"]

    def __str__(self):
        return f"{self.name} - {self.city}"


class Platform(models.Model):
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PriceSnapshot(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="price_snapshots",
    )
    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
        related_name="price_snapshots",
    )

    lowest_price = models.DecimalField(max_digits=10, decimal_places=2)
    average_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    currency = models.CharField(max_length=10, default="USD")

    listing_count = models.PositiveIntegerField(default=0)
    captured_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-captured_at"]
        indexes = [
            models.Index(fields=["event", "platform", "captured_at"]),
        ]

    def __str__(self):
        return f"{self.event.name} - {self.platform.name} - ${self.lowest_price}"


class TrackedEvent(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="tracked_events",
    )

    email = models.EmailField()
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["event", "email"]

    def __str__(self):
        return f"{self.email} tracking {self.event.name}"