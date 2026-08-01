from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone

from app.database import get_db
from app import models


router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)



@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db)
):

    # -----------------------
    # Total Leads
    # -----------------------

    total_leads = (
        db.query(models.Lead)
        .count()
    )


    # -----------------------
    # Active Conversations
    # -----------------------

    active_conversations = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.is_ai_active == True
        )
        .count()
    )



    # -----------------------
    # Bookings This Month
    # -----------------------

    now = datetime.now(timezone.utc)

    first_day = datetime(
        now.year,
        now.month,
        1,
        tzinfo=timezone.utc
    )


    bookings_this_month = (
        db.query(models.Booking)
        .filter(
            models.Booking.created_at >= first_day
        )
        .count()
    )



    # -----------------------
    # Conversion Rate
    # -----------------------

    booked_leads = (
        db.query(models.Lead)
        .filter(
            models.Lead.status == "booked"
        )
        .count()
    )


    conversion_rate = 0

    if total_leads > 0:
        conversion_rate = round(
            (booked_leads / total_leads) * 100,
            2
        )



    # -----------------------
    # Lead Sources
    # -----------------------

    sources = (
        db.query(
            models.Lead.platform,
            func.count(models.Lead.id)
        )
        .group_by(
            models.Lead.platform
        )
        .all()
    )


    lead_sources = {}

    for platform, count in sources:
        lead_sources[str(platform.value)] = count



    # -----------------------
    # Recent Leads
    # -----------------------

    recent_leads = (
        db.query(models.Lead)
        .order_by(
            models.Lead.created_at.desc()
        )
        .limit(5)
        .all()
    )



    return {

        "total_leads": total_leads,

        "active_conversations": active_conversations,

        "bookings_this_month": bookings_this_month,

        "conversion_rate": conversion_rate,


        "lead_sources": lead_sources,


        "recent_leads": [

            {
                "id": lead.id,
                "name": lead.full_name,
                "phone": lead.phone,
                "platform": lead.platform.value,
                "status": lead.status.value,
                "created_at": lead.created_at
            }

            for lead in recent_leads
        ]
    }