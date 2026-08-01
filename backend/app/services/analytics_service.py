from sqlalchemy.orm import Session
from app import models

def get_dashboard_stats(db: Session):
    return {
        "total_leads": db.query(models.Lead).count(),
        "new_leads": db.query(models.Lead).filter(models.Lead.status == "new").count(),
        "qualified_leads": db.query(models.Lead).filter(models.Lead.status == "qualified").count(),
        "conversations": db.query(models.Conversation).count(),
        "appointments": db.query(models.Appointment).count(),
        "calls_completed": db.query(models.Call).filter(models.Call.status == "completed").count(),
    }
