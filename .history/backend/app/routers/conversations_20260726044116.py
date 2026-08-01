from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app import models, schemas
from app.services.ai_service import get_ai_response

router = APIRouter(prefix="/conversations", tags=["conversations"])

@router.get("/", response_model=List[schemas.ConversationOut])
def get_conversations(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Conversation).options(
        joinedload(models.Conversation.lead),
        joinedload(models.Conversation.messages)
    ).order_by(models.Conversation.updated_at.desc()).offset(skip).limit(limit).all()

@router.get("/{conv_id}", response_model=schemas.ConversationOut)
def get_conversation(conv_id: int, db: Session = Depends(get_db)):
    conv = db.query(models.Conversation).options(
        joinedload(models.Conversation.lead),
        joinedload(models.Conversation.messages)
    ).filter(models.Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv

@router.post("/{conv_id}/send")
def send_message(conv_id: int, req: schemas.SendMessageRequest, db: Session = Depends(get_db)):
    """ادمین دستی پیام بفرسته"""
    conv = db.query(models.Conversation).filter(models.Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Not found")

    msg = models.Message(conversation_id=conv_id, role="admin", content=req.content)
    db.add(msg)
    db.commit()
    return {"ok": True}

@router.put("/{conv_id}/toggle-ai")
def toggle_ai(conv_id: int, db: Session = Depends(get_db)):
    """AI رو روشن/خاموش کن"""
    conv = db.query(models.Conversation).filter(models.Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Not found")
    conv.is_ai_active = not conv.is_ai_active
    db.commit()
    return {"is_ai_active": conv.is_ai_active}
