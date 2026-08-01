from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(prefix="/exports", tags=["exports"])

@router.get("/leads/json")
def export_leads_json(db: Session = Depends(get_db)):
    leads = db.query(models.Lead).all()
    return {
        "count": len(leads),
        "data": [
            {
                "id": l.id,
                "name": l.full_name,
                "phone": l.phone,
                "platform": str(l.platform),
                "status": str(l.status),
                "budget": l.budget,
                "created_at": l.created_at.isoformat() if l.created_at else None,
            }
            for l in leads
        ]
    }

@router.get("/conversations/json")
def export_conversations_json(db: Session = Depends(get_db)):
    convs = db.query(models.Conversation).all()
    return {
        "count": len(convs),
        "data": [
            {
                "id": c.id,
                "platform": str(c.platform),
                "lead": c.lead.full_name if c.lead else "Unknown",
                "messages_count": len(c.messages),
                "created_at": c.created_at.isoformat() if c.created_at else None,
            }
            for c in convs
        ]
    }

@router.get("/bookings/json")
def export_bookings_json(db: Session = Depends(get_db)):
    bookings = db.query(models.Booking).all()
    return {
        "count": len(bookings),
        "data": [
            {
                "id": b.id,
                "lead": b.lead.full_name if b.lead else "Unknown",
                "scheduled_at": b.scheduled_at.isoformat() if b.scheduled_at else None,
                "status": b.status,
                "duration": b.duration_minutes,
            }
            for b in bookings
        ]
    }
