from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timezone

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/bookings",
    tags=["bookings"]
)



# =====================================================
# GET ALL BOOKINGS
# =====================================================

response.append({

    "id": booking.id,


    "customer": {

        "id": booking.lead.id
        if booking.lead else None,

        "name": booking.lead.full_name
        if booking.lead else "Unknown Customer",

        "phone": booking.lead.phone
        if booking.lead else None,

        "telegram_username":
            booking.lead.telegram_username
            if booking.lead else None

    },


    "service":
        booking.service
        or "AI Consultation",


    "scheduled_at":
        booking.scheduled_at,


    "duration_minutes":
        booking.duration_minutes
        or 30,


    "status":
        booking.status,


    "notes":
        booking.notes,


    "created_at":
        booking.created_at,


    "updated_at":
        getattr(
            booking,
            "updated_at",
            None
        )

})


# =====================================================
# CREATE BOOKING
# =====================================================

@router.post("/")
def create_booking(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db)
):


    conflict = (
        db.query(models.Booking)
        .filter(

            models.Booking.scheduled_at
            ==
            booking.scheduled_at,

            models.Booking.status
            !=
            "cancelled"

        )
        .first()
    )


    if conflict:

        raise HTTPException(
            status_code=400,
            detail="This time slot is already booked"
        )



    new_booking = models.Booking(

        lead_id =
            booking.lead_id,

        service =
            booking.service,

        scheduled_at =
            booking.scheduled_at,

        duration_minutes =
            booking.duration_minutes,

        status =
            "confirmed",

        notes =
            booking.notes

    )


    db.add(new_booking)



    lead = (
        db.query(models.Lead)
        .filter(
            models.Lead.id ==
            booking.lead_id
        )
        .first()
    )


    if lead:

        lead.status = "booked"



    db.commit()

    db.refresh(new_booking)



    return {

        "success": True,

        "booking_id":
            new_booking.id

    }





# =====================================================
# UPDATE BOOKING
# =====================================================

@router.patch("/{booking_id}")
def update_booking(
    booking_id: int,
    data: dict,
    db: Session = Depends(get_db)
):


    booking = (
        db.query(models.Booking)
        .filter(
            models.Booking.id ==
            booking_id
        )
        .first()
    )


    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )



    allowed = [

        "status",

        "scheduled_at",

        "notes",

        "service",

        "duration_minutes"

    ]



    for key,value in data.items():

        if key in allowed:

            setattr(
                booking,
                key,
                value
            )



    if hasattr(
        booking,
        "updated_at"
    ):

        booking.updated_at = datetime.now(
            timezone.utc
        )



    db.commit()



    return {

        "success": True,

        "message":
            "Booking updated"

    }





# =====================================================
# DELETE / CANCEL BOOKING
# =====================================================

@router.delete("/{booking_id}")
def cancel_booking(
    booking_id:int,
    db:Session = Depends(get_db)
):


    booking = (
        db.query(models.Booking)
        .filter(
            models.Booking.id ==
            booking_id
        )
        .first()
    )


    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )


    booking.status = "cancelled"


    db.commit()



    return {

        "success":True,

        "message":
            "Booking cancelled"

    }