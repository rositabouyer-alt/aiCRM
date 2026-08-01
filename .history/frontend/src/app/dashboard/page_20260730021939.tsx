from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import func
from typing import List

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"]
)


# =====================================
# GET ALL CONVERSATIONS
# =====================================

@router.get("/", response_model=List[schemas.ConversationOut])
def get_conversations(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):

    conversations = (
        db.query(models.Conversation)
        .options(
            joinedload(models.Conversation.lead),
            joinedload(models.Conversation.messages)
        )
        .order_by(
            models.Conversation.updated_at.desc().nullslast()
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    return conversations


# =====================================
# GET SINGLE CONVERSATION
# =====================================

@router.get("/{conv_id}", response_model=schemas.ConversationOut)
def get_conversation(
    conv_id: int,
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(models.Conversation)
        .options(
            joinedload(models.Conversation.lead),
            joinedload(models.Conversation.messages)
        )
        .filter(models.Conversation.id == conv_id)
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    conversation.messages.sort(
        key=lambda x: x.created_at
    )

    return conversation


# =====================================
# ADMIN SEND MESSAGE
# =====================================

@router.post("/{conv_id}/send")
def send_message(
    conv_id: int,
    req: schemas.SendMessageRequest,
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(models.Conversation)
        .filter(models.Conversation.id == conv_id)
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    message = models.Message(
        conversation_id=conversation.id,
        role="admin",
        content=req.content
    )

    db.add(message)

    conversation.updated_at = func.now()

    db.commit()
    db.refresh(message)

    return {
        "success": True,
        "message": message.content
    }


# =====================================
# TOGGLE AI
# =====================================

@router.put("/{conv_id}/toggle-ai")
def toggle_ai(
    conv_id: int,
    db: Session = Depends(get_db)
):

    conversation = (
        db.query(models.Conversation)
        .filter(models.Conversation.id == conv_id)
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    conversation.is_ai_active = not conversation.is_ai_active
    conversation.updated_at = func.now()

    db.commit()

    return {
        "success": True,
        "is_ai_active": conversation.is_ai_active
    }