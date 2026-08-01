from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/bookings",
    tags=["bookings"]
)



# ==========================
# GET ALL BOOKINGS
# ==========================

@router.get("/")
def get_bookings(
    db: Session = Depends(get_db)
):

    bookings = (
        db.query(models.Booking)
        .options(
            joinedload(models.Booking.lead)
        )
        .order_by(
            models.Booking.scheduled_at
        )
        .all()
    )


    result = []


    for booking in bookings:

        result.append({

            "id": booking.id,

            "service": booking.service,

            "scheduled_at": booking.scheduled_at,

            "duration_minutes": booking.duration_minutes,

            "status": booking.status,

            "notes": booking.notes,

            "created_at": booking.created_at,


            "customer": {

                "id": booking.lead.id,

                "full_name": booking.lead.full_name,

                "phone": booking.lead.phone,

                "platform": (
                    booking.lead.platform.value
                    if booking.lead.platform
                    else None
                )

            }
            if booking.lead
            else None

        })


    return result




# ==========================
# CREATE BOOKING
# ==========================

@router.post("/")
def create_booking(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db)
):


    existing = (
        db.query(models.Booking)
        .filter(
            models.Booking.scheduled_at == booking.scheduled_at,
            models.Booking.status != "cancelled"
        )
        .first()
    )


    if existing:

        raise HTTPException(
            status_code=400,
            detail="This time is already booked"
        )



    db_booking = models.Booking(
        **booking.model_dump()
    )


    db.add(db_booking)


    lead = (
        db.query(models.Lead)
        .filter(
            models.Lead.id == booking.lead_id
        )
        .first()
    )


    if lead:

        lead.status = "booked"



    db.commit()


    db.refresh(db_booking)


    return {

        "message": "Booking created",

        "id": db_booking.id

    }




# ==========================
# UPDATE STATUS
# ==========================

@router.put("/{booking_id}/status")
def update_status(
    booking_id: int,
    status: str,
    db: Session = Depends(get_db)
):


    booking = (
        db.query(models.Booking)
        .filter(
            models.Booking.id == booking_id
        )
        .first()
    )


    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )


    booking.status = status


    db.commit()


    return {
        "ok": True
    }