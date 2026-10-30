from sqlalchemy import (
    Column, Integer, String, Numeric, Boolean,
    Date, TIMESTAMP, ForeignKey, CheckConstraint, text
)
from sqlalchemy.orm import relationship
from src.repository.database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id   = Column(Integer, primary_key=True, autoincrement=True)
    customer_name  = Column(String(100), nullable=False)
    customer_email = Column(String(100), nullable=False, unique=True)
    customer_phone = Column(String(15), nullable=True)
    is_active      = Column(Boolean, nullable=False, default=True, server_default=text("TRUE"))
    created_at     = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by     = Column(String(100), nullable=False, server_default=text("'system'"))
    updated_at     = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by     = Column(String(100), nullable=False, server_default=text("'system'"))

    bookings = relationship("Booking", back_populates="customer")


class Room(Base):
    __tablename__ = "rooms"

    __table_args__ = (
        CheckConstraint(
            "room_type IN ('Standard', 'Deluxe', 'Executive', 'Suite', 'Presidential Suite')",
            name="ck_rooms_room_type"
        ),
    )

    room_id        = Column(Integer, primary_key=True, autoincrement=True)
    room_number    = Column(String(10), nullable=False, unique=True)
    room_type      = Column(String(50), nullable=False)
    price_per_night = Column(Numeric(10, 2), nullable=False)
    is_active      = Column(Boolean, nullable=False, default=True, server_default=text("TRUE"))
    created_at     = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by     = Column(String(100), nullable=False, server_default=text("'system'"))
    updated_at     = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by     = Column(String(100), nullable=False, server_default=text("'system'"))

    bookings = relationship("Booking", back_populates="room")


class Booking(Base):
    __tablename__ = "bookings"

    __table_args__ = (
        CheckConstraint(
            "check_out > check_in",
            name="ck_bookings_checkout_after_checkin"
        ),
    )

    booking_id  = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    room_id     = Column(Integer, ForeignKey("rooms.room_id"), nullable=False)
    check_in    = Column(Date, nullable=False)
    check_out   = Column(Date, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    is_active   = Column(Boolean, nullable=False, default=True, server_default=text("TRUE"))
    created_at  = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by  = Column(String(100), nullable=False, server_default=text("'system'"))
    updated_at  = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by  = Column(String(100), nullable=False, server_default=text("'system'"))

    customer = relationship("Customer", back_populates="bookings")
    room     = relationship("Room", back_populates="bookings")
