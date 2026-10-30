# Hotel Room Booking System

## Overview

A hotel management system that allows customers to book rooms, retrieve booking details, and cancel bookings via a REST API.

---

## Actors

- **Customer** — a person who books a hotel room
- **System** — the API that handles bookings, customer registration, and room management

---

## Use Cases

### 1. Create a Booking

A customer provides their details along with a room and date range. The system handles the rest.

**Steps:**
1. Customer submits their name, email, phone, room ID, check-in and check-out dates
2. System checks if the customer email already exists
   - If yes → reuses the existing customer record
   - If no → registers a new customer automatically
3. System validates the room exists
4. System checks the room is available for the requested dates (no overlapping active bookings)
5. System calculates total nights and total price
6. System creates the booking and returns full booking details

**Validations:**
- `check_in` must not be in the past
- `check_out` must be after `check_in`
- Room must exist and be available for the selected dates

**Outcomes:**
- `201 Created` — booking created successfully
- `404 Not Found` — room does not exist
- `409 Conflict` — room is not available for the selected dates
- `422 Unprocessable Entity` — invalid input (missing fields, bad dates)

---

### 2. Retrieve a Booking

A client fetches the full details of an existing booking by its ID.

**Steps:**
1. Client provides a booking ID
2. System looks up the booking (only active bookings are returned)
3. System returns booking details along with customer and room information

**Outcomes:**
- `200 OK` — booking details returned
- `404 Not Found` — booking does not exist or has been cancelled

---

### 3. Cancel a Booking

A customer cancels an existing booking.

**Steps:**
1. Customer provides the booking ID to cancel
2. System looks up the booking (only active bookings can be cancelled)
3. System performs a soft delete — sets `is_active = FALSE`, retains the record for audit purposes
4. System returns a confirmation

**Outcomes:**
- `200 OK` — booking cancelled successfully
- `404 Not Found` — booking does not exist or already cancelled

---

## Business Rules

- A customer is identified by their email address — the same email always maps to the same customer record
- A room cannot be double-booked for overlapping dates
- Cancelled bookings are not deleted from the database — they are flagged as inactive
- Total price is calculated as `price_per_night × number of nights`
- All tables carry audit columns: `created_at`, `created_by`, `updated_at`, `updated_by`, `is_active`

---

## Room Types and Pricing

| Room Type         | Price per Night |
|-------------------|----------------|
| Standard          | ₹2,000          |
| Deluxe            | ₹3,500          |
| Executive         | ₹4,500          |
| Suite             | ₹6,000          |
| Presidential Suite| ₹10,000         |

---

## Project Structure

```
room_booking/
├── requirements.txt
├── src/
│   ├── main.py
│   ├── settings.py
│   ├── .env
│   ├── migrations/
│   │   └── migrations.py
│   ├── repository/
│   │   ├── database.py
│   │   └── repository.py
│   ├── schemas/
│   │   └── schemas.py
│   ├── models/
│   │   ├── request_dto.py
│   │   └── response_dto.py
│   ├── services/
│   │   └── services.py
│   ├── routers/
│   │   └── routers.py
│   └── utils/
│       ├── error_codes.py
│       ├── exceptions.py
│       └── utils.py
```
