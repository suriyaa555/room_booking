from src.repository.database import SessionLocal, engine
from src.schemas.schemas import Base, Room


def seed_rooms(db):
    """Seed the rooms table with initial room data if it is empty."""
    existing = db.query(Room).first()
    if existing:
        print("Rooms table already has data. Skipping seed.")
        return

    rooms = [
        Room(room_number="101", room_type="Standard",           price_per_night=2000.00),
        Room(room_number="102", room_type="Standard",           price_per_night=2000.00),
        Room(room_number="201", room_type="Deluxe",             price_per_night=3500.00),
        Room(room_number="202", room_type="Deluxe",             price_per_night=3500.00),
        Room(room_number="301", room_type="Executive",          price_per_night=4500.00),
        Room(room_number="302", room_type="Executive",          price_per_night=4500.00),
        Room(room_number="401", room_type="Suite",              price_per_night=6000.00),
        Room(room_number="402", room_type="Suite",              price_per_night=6000.00),
        Room(room_number="501", room_type="Presidential Suite", price_per_night=10000.00),
        Room(room_number="502", room_type="Presidential Suite", price_per_night=10000.00),
    ]

    db.add_all(rooms)
    db.commit()
    print(f"Seeded {len(rooms)} rooms successfully.")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_rooms(db)
    finally:
        db.close()
