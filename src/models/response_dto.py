from pydantic import BaseModel
from datetime import date
from typing import Optional
from decimal import Decimal


class BookingCreateResponseDTO(BaseModel):
    message: str
    booking_id: int
    customer_id: int
    customer_name: str
    room_id: int
    room_number: str
    room_type: str
    check_in: date
    check_out: date
    total_nights: int
    price_per_night: Decimal
    total_price: Decimal

    model_config = {"from_attributes": True}


class BookingDetailResponseDTO(BaseModel):
    booking_id: int
    customer_id: int
    customer_name: str
    customer_email: str
    customer_phone: Optional[str]
    room_id: int
    room_number: str
    room_type: str
    price_per_night: Decimal
    check_in: date
    check_out: date
    total_price: Decimal

    model_config = {"from_attributes": True}


class BookingCancelResponseDTO(BaseModel):
    message: str
    booking_id: int
