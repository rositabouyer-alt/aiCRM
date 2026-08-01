from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.get("/", response_model=List[schemas.BookingOut])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(models.Booking).order_by(models.Booking.scheduled_at).all()

@router.post("/", response_model=schemas.BookingOut)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    # چک کن تداخل نداشته باشه
    existing = db.query(models.Booking).filter(
        models.Booking.scheduled_at == booking.scheduled_at,
        models.Booking.status != "cancelled"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="این زمان قبلاً رزرو شده")

    db_booking = models.Booking(**booking.model_dump())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@router.put("/{booking_id}/status")
def update_status(booking_id: int, status: str, db: Session = Depends(get_db)):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Not found")
    booking.status = status
    db.commit()
    return {"ok": True}
