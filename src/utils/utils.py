from datetime import date
from decimal import Decimal


def calculate_total_nights(check_in: date, check_out: date) -> int:
    """Returns the number of nights between check_in and check_out."""
    return (check_out - check_in).days


def calculate_total_price(price_per_night: Decimal, total_nights: int) -> Decimal:
    """Returns the total price as price_per_night multiplied by total_nights."""
    return price_per_night * total_nights
