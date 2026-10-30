from fastapi import HTTPException, status
from src.utils import error_codes


def booking_not_found(booking_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error_code": error_codes.BOOKING_NOT_FOUND,
            "message": f"Booking with id {booking_id} not found.",
        },
    )


def room_not_found(room_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error_code": error_codes.ROOM_NOT_FOUND,
            "message": f"Room with id {room_id} not found.",
        },
    )


def room_not_available() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={
            "error_code": error_codes.ROOM_NOT_AVAILABLE,
            "message": "Room is not available for the selected dates.",
        },
    )
