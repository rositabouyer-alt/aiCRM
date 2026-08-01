from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from sqlalchemy.sql import func

from app.database import get_db
from app import models, schemas


router = APIRouter(
    prefix="/conversations",
    tags=["conversations"]
)


# =========================
# GET ALL CONVERSATIONS
# =========================

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
            models.Conversation.updated_at.desc()
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    return conversations



# =========================
# GET SINGLE CONVERSATION
# =========================

@router.get("/{conv_id}", response_model=schemas.ConversationOut)
def get_conversation(
    conv_id: int,
    db: Session = Depends(get_db)
):

    conv = (
        db.query(models.Conversation)
        .options(
            joinedload(models.Conversation.lead),
            joinedload(models.Conversation.messages)
        )
        .filter(
            models.Conversation.id == conv_id
        )
        .first()
    )


    if not conv:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


    return conv




# =========================
# ADMIN SEND MESSAGE
# =========================

@router.post("/{conv_id}/send")
def send_message(
    conv_id: int,
    req: schemas.SendMessageRequest,
    db: Session = Depends(get_db)
):

    conv = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.id == conv_id
        )
        .first()
    )


    if not conv:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )



    message = models.Message(
        conversation_id=conv.id,
        role="admin",
        content=req.content
    )


    db.add(message)


    # update conversation activity
    conv.updated_at = func.now()


    db.commit()


    return {
        "success": True
    }





# =========================
# TOGGLE AI
# =========================

@router.put("/{conv_id}/toggle-ai")
def toggle_ai(
    conv_id: int,
    db: Session = Depends(get_db)
):

    conv = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.id == conv_id
        )
        .first()
    )


    if not conv:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


    conv.is_ai_active = not conv.is_ai_active

    db.commit()


    return {
        "is_ai_active": conv.is_ai_active
    }