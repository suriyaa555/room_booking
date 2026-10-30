from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.routers.routers import router
from src.repository.database import Base, engine, SessionLocal
from src.migrations.migrations import seed_rooms


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables if they do not exist, then seed initial data
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_rooms(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Hotel Room Booking System",
    description=(
        "REST API for managing hotel room bookings. "
        "Supports creating bookings, retrieving booking details, "
        "and cancelling bookings."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)
