from sqlalchemy.orm import Session

from src.models.request_dto import BookingRequestDTO
from src.models.response_dto import (
    BookingCreateResponseDTO,
    BookingDetailResponseDTO,
    BookingCancelResponseDTO,
)
from src.repository import repository
from src.utils.exceptions import (
    booking_not_found,
    room_not_found,
    room_not_available,
)
from src.utils.utils import calculate_total_nights, calculate_total_price


def create_booking(db: Session, payload: BookingRequestDTO) -> BookingCreateResponseDTO:
    """
    Business logic for POST /bookings:
    1. Reuse existing customer by email, or create a new one.
    2. Validate the room exists.
    3. Check room availability (no overlapping active bookings).
    4. Calculate total_nights and total_price.
    5. Persist the booking and return the response.
    """
    # 1. Customer lookup / creation
    customer = repository.get_customer_by_email(db, payload.customer_email)
    if customer is None:
        customer = repository.create_customer(
            db,
            name=payload.customer_name,
            email=payload.customer_email,
            phone=payload.customer_phone,
        )

    # 2. Room validation
    room = repository.get_room_by_id(db, payload.room_id)
    if room is None:
        raise room_not_found(payload.room_id)

    # 3. Availability check
    available = repository.is_room_available(
        db,
        room_id=payload.room_id,
        check_in=payload.check_in,
        check_out=payload.check_out,
    )
    if not available:
        raise room_not_available()

    # 4. Pricing
    total_nights = calculate_total_nights(payload.check_in, payload.check_out)
    total_price = calculate_total_price(room.price_per_night, total_nights)

    # 5. Create booking
    booking = repository.create_booking(
        db,
        customer_id=customer.customer_id,
        room_id=room.room_id,
        check_in=payload.check_in,
        check_out=payload.check_out,
        total_price=total_price,
    )

    return BookingCreateResponseDTO(
        message="Booking created successfully",
        booking_id=booking.booking_id,
        customer_id=customer.customer_id,
        customer_name=customer.customer_name,
        room_id=room.room_id,
        room_number=room.room_number,
        room_type=room.room_type,
        check_in=booking.check_in,
        check_out=booking.check_out,
        total_nights=total_nights,
        price_per_night=room.price_per_night,
        total_price=booking.total_price,
    )


def get_booking(db: Session, booking_id: int) -> BookingDetailResponseDTO:
    """
    Business logic for GET /bookings/{booking_id}:
    Fetch the active booking with joined customer and room data.
    """
    booking = repository.get_booking_by_id(db, booking_id)
    if booking is None:
        raise booking_not_found(booking_id)

    return BookingDetailResponseDTO(
        booking_id=booking.booking_id,
        customer_id=booking.customer.customer_id,
        customer_name=booking.customer.customer_name,
        customer_email=booking.customer.customer_email,
        customer_phone=booking.customer.customer_phone,
        room_id=booking.room.room_id,
        room_number=booking.room.room_number,
        room_type=booking.room.room_type,
        price_per_night=booking.room.price_per_night,
        check_in=booking.check_in,
        check_out=booking.check_out,
        total_price=booking.total_price,
    )


def cancel_booking(db: Session, booking_id: int) -> BookingCancelResponseDTO:
    """
    Business logic for DELETE /bookings/{booking_id}:
    Soft-delete the booking by setting is_active=False.
    """
    booking = repository.get_booking_by_id(db, booking_id)
    if booking is None:
        raise booking_not_found(booking_id)

    repository.cancel_booking(db, booking)

    return BookingCancelResponseDTO(
        message="Booking cancelled successfully",
        booking_id=booking_id,
    )
