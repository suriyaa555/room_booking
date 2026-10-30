from pydantic import BaseModel, EmailStr, field_validator
from datetime import date
from typing import Optional


class BookingRequestDTO(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: Optional[str] = None
    room_id: int
    check_in: date
    check_out: date

    @field_validator("customer_name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("customer_name must not be blank.")
        return v.strip()

    @field_validator("check_in")
    @classmethod
    def checkin_must_not_be_in_the_past(cls, check_in: date) -> date:
        if check_in < date.today():
            raise ValueError("check_in must not be in the past.")
        return check_in

    @field_validator("check_out")
    @classmethod
    def checkout_must_be_after_checkin(cls, check_out: date, info) -> date:
        check_in = info.data.get("check_in")
        if check_in and check_out <= check_in:
            raise ValueError("check_out must be after check_in.")
        return check_out
