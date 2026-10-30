from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.repository.database import get_db
from src.models.request_dto import BookingRequestDTO
from src.models.response_dto import (
    BookingCreateResponseDTO,
    BookingDetailResponseDTO,
    BookingCancelResponseDTO,
)
from src.services import services

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post(
    "",
    response_model=BookingCreateResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new booking",
)
def create_booking(
    payload: BookingRequestDTO,
    db: Session = Depends(get_db),
) -> BookingCreateResponseDTO:
    """
    Create a hotel room booking.

    - Reuses an existing customer if the email already exists, otherwise
      registers a new customer automatically.
    - Validates that the room exists and is available for the requested dates.
    - Calculates total_price as price_per_night × number of nights.
    """
    return services.create_booking(db, payload)


@router.get(
    "/{booking_id}",
    response_model=BookingDetailResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Retrieve booking details",
)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
) -> BookingDetailResponseDTO:
    """
    Fetch full details of an active booking by its ID, including
    customer and room information.
    """
    return services.get_booking(db, booking_id)


@router.delete(
    "/{booking_id}",
    response_model=BookingCancelResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Cancel a booking",
)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
) -> BookingCancelResponseDTO:
    """
    Cancel an existing booking by performing a soft delete
    (sets is_active = FALSE). The record is retained for audit purposes.
    """
    return services.cancel_booking(db, booking_id)
