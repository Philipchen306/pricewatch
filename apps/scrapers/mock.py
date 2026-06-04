from decimal import Decimal
from random import randint, uniform

def fetch_mock_price(event, platform):
    base_price = randint(80, 250)
    lowest_price = Decimal(str(round(base_price + uniform(-20, 20), 2)))

    return {
        "event": event,
        "platform": platform,
        "lowest_price": lowest_price,
        "average_price": lowest_price + Decimal("25.00"),
        "currency": "USD",
        "listing_count": randint(20, 300),
    }