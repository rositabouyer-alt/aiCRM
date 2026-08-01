from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone, timedelta

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

    # ==========================
    # Total Leads
    # ==========================

    total_leads = (
        db.query(models.Lead)
        .count()
    )


    # ==========================
    # Active Conversations
    # ==========================

    active_conversations = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.is_ai_active.is_(True)
        )
        .count()
    )


    # ==========================
    # Bookings This Month
    # ==========================

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


    # ==========================
    # Conversion Rate
    # ==========================

    booked_leads = (
        db.query(models.Lead)
        .filter(
            models.Lead.status == "booked"
        )
        .count()
    )


    conversion_rate = 0

    if total_leads:
        conversion_rate = round(
            (booked_leads / total_leads) * 100,
            2
        )


    # ==========================
    # Lead Sources
    # ==========================

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

        if platform:
            lead_sources[platform.value] = count



    # ==========================
    # Recent Leads
    # ==========================

    recent_leads = (
        db.query(models.Lead)
        .order_by(
            models.Lead.created_at.desc()
        )
        .limit(5)
        .all()
    )


    # ==========================
    # Last 7 Days Chart Data
    # ==========================

    seven_days_ago = (
        datetime.now(timezone.utc)
        - timedelta(days=7)
    )


    daily_leads = (
        db.query(
            func.date(models.Lead.created_at),
            func.count(models.Lead.id)
        )
        .filter(
            models.Lead.created_at >= seven_days_ago
        )
        .group_by(
            func.date(models.Lead.created_at)
        )
        .all()
    )


    chart_data = []

    for date, count in daily_leads:

        chart_data.append(
            {
                "date": str(date),
                "leads": count
            }
        )



    return {

        "total_leads": total_leads,


        "active_conversations": active_conversations,


        "bookings_this_month": bookings_this_month,


        "conversion_rate": conversion_rate,


        "lead_sources": lead_sources,


        "chart_data": chart_data,


        "recent_leads": [

            {
                "id": lead.id,

                "name": lead.full_name,

                "phone": lead.phone,

                "platform": (
                    lead.platform.value
                    if lead.platform
                    else None
                ),

                "status": (
                    lead.status.value
                    if lead.status
                    else None
                ),

                "created_at": lead.created_at
            }

            for lead in recent_leads
        ]
    }