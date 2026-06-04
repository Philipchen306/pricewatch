import os 
import requests 
from decimal import Decimal
from django.utils.dateparse import parse_datetime, parse_date
from django.utils import timezone

TICKETMASTER_BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

def search_ticketmaster_events(keyword="Chicago Cubs", city="Chicago", size=10):
    api_key = os.getenv("TICKETMASTER_API_KEY")

    if not api_key:
        raise ValueError("TICKETMASTER_API_KEY is missing in .env")

    params = {
        "apikey": api_key,
        "keyword": keyword,
        "city": city,
        "countryCode": "US",
        "size": size,
        "sort": "date,asc",
    }

    response = requests.get(TICKETMASTER_BASE_URL, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    events = data.get("_embedded", {}).get("events", [])

    return [normalize_ticketmaster_event(event) for event in events]

def normalize_ticketmaster_event(raw_event):
    dates = raw_event.get("dates", {}).get("start", {})
    local_date = dates.get("localDate")
    local_time = dates.get("localTime", "00:00:00")

    event_date = None
    if local_date:
        event_date = parse_datetime(f"{local_date}T{local_time}")
        if event_date and timezone.is_naive(event_date):
            event_date = timezone.make_aware(event_date)
    
    venues = raw_event.get("_embedded", {}).get("venues", [])
    venue = venues[0] if venues else {}

    city = venue.get("city", {}).get("name", "")
    state = venue.get("state", {}).get("name", "")
    venue_name = venue.get("name", "")
    address = venue.get("address", {}).get("line1", "")

    location = venue.get("location", {})
    latitude = location.get("latitude")
    longitude = location.get("longitude")

    classifications = raw_event.get("classifications", [])
    classification = classifications[0] if classifications else {}

    segment = classification.get("segment", {}).get("name", "")
    genre = classification.get("genre", {}).get("name", "")
    sub_genre = classification.get("subGenre", {}).get("name", "")

    category = "other"
    if segment.lower() == "sports":
        category = "sports"
    elif segment.lower() == "music":
        category = "concert"

    images = raw_event.get("images", [])
    image_url = images[0]["url"] if images else ""

    price_ranges = raw_event.get("priceRanges", [])
    lowest_price = None
    highest_price = None
    currency = "USD"

    if price_ranges:
        price_range = price_ranges[0]
        if price_range.get("min") is not None:
            lowest_price = Decimal(str(price_range["min"]))
        if price_range.get("max") is not None:
            highest_price = Decimal(str(price_range["max"]))
        currency = price_range.get("currency", "USD")

    return {
        "external_id": raw_event.get("id"),
        "name": raw_event.get("name", ""),
        "category": category,
        "genre": genre,
        "sub_genre": sub_genre,
        "city": city,
        "state": state,
        "venue": venue_name,
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
        "event_date": event_date,
        "source": "ticketmaster",
        "source_url": raw_event.get("url", ""),
        "image_url": image_url,
        "lowest_price": lowest_price,
        "highest_price": highest_price,
        "currency": currency,
    }
