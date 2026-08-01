from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

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

    total_leads = db.query(
        models.Lead
    ).count()


    active_conversations = db.query(
        models.Conversation
    ).filter(
        models.Conversation.is_ai_active == True
    ).count()


    total_conversations = db.query(
        models.Conversation
    ).count()


    total_bookings = db.query(
        models.Booking
    ).count()


    conversion_rate = 0

    if total_leads > 0:
        conversion_rate = (
            total_bookings / total_leads
        ) * 100


    telegram_leads = db.query(
        models.Lead
    ).filter(
        models.Lead.platform == "telegram"
    ).count()



    return {

        "total_leads": total_leads,

        "active_conversations": active_conversations,

        "total_conversations": total_conversations,

        "total_bookings": total_bookings,

        "telegram_leads": telegram_leads,

        "conversion_rate": round(
            conversion_rate,
            2
        )
    }