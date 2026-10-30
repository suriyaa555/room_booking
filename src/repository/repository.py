from datetime import date, datetime
from sqlalchemy.orm import Session
from src.schemas.schemas import Customer, Room, Booking


# --------------------------------------------------------------------------- #
# Customer queries
# --------------------------------------------------------------------------- #

def get_customer_by_email(db: Session, email: str) -> Customer | None:
    """Return an active customer matching the given email, or None."""
    return (
        db.query(Customer)
        .filter(Customer.customer_email == email, Customer.is_active == True)
        .first()
    )


def create_customer(
    db: Session,
    name: str,
    email: str,
    phone: str | None,
) -> Customer:
    """Insert a new customer record and return it."""
    customer = Customer(
        customer_name=name,
        customer_email=email,
        customer_phone=phone,
    )
    db.add(customer)
    db.flush()   # populate customer_id before using it in the booking
    return customer


# --------------------------------------------------------------------------- #
# Room queries
# --------------------------------------------------------------------------- #

def get_room_by_id(db: Session, room_id: int) -> Room | None:
    """Return an active room by primary key, or None."""
    return (
        db.query(Room)
        .filter(Room.room_id == room_id, Room.is_active == True)
        .first()
    )


# --------------------------------------------------------------------------- #
# Booking queries
# --------------------------------------------------------------------------- #

def is_room_available(
    db: Session,
    room_id: int,
    check_in: date,
    check_out: date,
) -> bool:
    """
    Return True when no active booking overlaps the requested date range
    for the given room.

    Overlap condition:
        existing.check_in  < requested.check_out
        AND
        existing.check_out > requested.check_in
    """
    conflict = (
        db.query(Booking)
        .filter(
            Booking.room_id == room_id,
            Booking.is_active == True,
            Booking.check_in < check_out,
            Booking.check_out > check_in,
        )
        .first()
    )
    return conflict is None


def create_booking(
    db: Session,
    customer_id: int,
    room_id: int,
    check_in: date,
    check_out: date,
    total_price: float,
) -> Booking:
    """Insert a new booking record and return it with relationships loaded."""
    booking = Booking(
        customer_id=customer_id,
        room_id=room_id,
        check_in=check_in,
        check_out=check_out,
        total_price=total_price,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_booking_by_id(db: Session, booking_id: int) -> Booking | None:
    """Return an active booking by primary key with customer and room joined."""
    return (
        db.query(Booking)
        .filter(Booking.booking_id == booking_id, Booking.is_active == True)
        .first()
    )


def cancel_booking(db: Session, booking: Booking) -> Booking:
    """Soft-delete a booking by setting is_active=False and updating updated_at."""
    booking.is_active = False
    booking.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(booking)
    return booking
