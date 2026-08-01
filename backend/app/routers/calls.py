from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/calls", tags=["calls"])

class CallRequest(BaseModel):
    conversation_id: int
    duration_minutes: int = 0
    notes: str = ""

@router.post("/log")
def log_call(req: CallRequest, db: Session = Depends(get_db)):
    try:
        conv = db.query(models.Conversation).filter(models.Conversation.id == req.conversation_id).first()
        if not conv:
            return {"error": "Conversation not found"}
        
        # Save as message
        call_msg = models.Message(
            conversation_id=req.conversation_id,
            role="system",
            content=f"📞 تماس تلفنی: {req.duration_minutes} دقیقه | یادداشت: {req.notes}"
        )
        db.add(call_msg)
        
        # Update lead status
        if conv.lead:
            conv.lead.status = "qualified"
        
        db.commit()
        return {"ok": True, "message": "Call logged"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/{conv_id}")
def get_calls(conv_id: int, db: Session = Depends(get_db)):
    try:
        messages = db.query(models.Message).filter(
            models.Message.conversation_id == conv_id,
            models.Message.role == "system"
        ).all()
        
        return {
            "count": len(messages),
            "calls": [{"id": m.id, "content": m.content, "time": m.created_at} for m in messages]
        }
    except:
        return {"count": 0, "calls": []}
