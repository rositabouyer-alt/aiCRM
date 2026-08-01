from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timezone
from typing import Optional

from app.database import get_db
from app import models


router = APIRouter(
    prefix="/conversations",
    tags=["conversations"]
)


# =====================================================
# GET ALL CONVERSATIONS
# =====================================================

@router.get("/")
def get_conversations(
    search: Optional[str] = None,
    platform: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):

    query = (
        db.query(models.Conversation)
        .options(
            joinedload(models.Conversation.lead),
            joinedload(models.Conversation.messages)
        )
    )


    if platform:
        query = query.filter(
            models.Conversation.platform == platform
        )


    if status:
        query = query.filter(
            models.Conversation.status == status
        )


    if search:

        query = (
            query
            .join(models.Conversation.lead)
            .filter(
                models.Lead.full_name.ilike(
                    f"%{search}%"
                )
            )
        )


    conversations = (
        query
        .order_by(
            models.Conversation.updated_at.desc()
        )
        .offset(
            (page - 1) * limit
        )
        .limit(limit)
        .all()
    )


    result = []


    for conversation in conversations:

        lead = conversation.lead


        messages = sorted(
            conversation.messages or [],
            key=lambda x: x.created_at or datetime.min
        )


        result.append({

            "id": conversation.id,


            "platform":
                conversation.platform.value
                if conversation.platform
                else None,


            "platform_chat_id":
                conversation.platform_chat_id,


            "status":
                conversation.status,


            "is_ai_active":
                conversation.is_ai_active,


            "created_at":
                conversation.created_at,


            "updated_at":
                conversation.updated_at,


            "lead": {

                "id": lead.id,

                "full_name":
                    lead.full_name,

                "phone":
                    lead.phone,

                "email":
                    lead.email

            }
            if lead else None,


            "messages": [

                {

                    "id": msg.id,

                    "role": msg.role,

                    "content": msg.content,

                    "created_at":
                        msg.created_at

                }

                for msg in messages

            ]

        })


    return {

        "page": page,

        "limit": limit,

        "count": len(result),

        "data": result

    }





# =====================================================
# GET SINGLE CONVERSATION
# =====================================================

@router.get("/{conversation_id}")
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):


    conversation = (

        db.query(models.Conversation)

        .options(
            joinedload(models.Conversation.lead),
            joinedload(models.Conversation.messages)
        )

        .filter(
            models.Conversation.id == conversation_id
        )

        .first()

    )


    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


    lead = conversation.lead


    return {


        "id": conversation.id,


        "platform":
            conversation.platform.value
            if conversation.platform
            else None,


        "status":
            conversation.status,


        "is_ai_active":
            conversation.is_ai_active,


        "lead": {

            "id": lead.id,

            "full_name":
                lead.full_name,

            "phone":
                lead.phone,

            "email":
                lead.email

        }
        if lead else None,


        "messages": [

            {

                "id": msg.id,

                "role":
                    msg.role,

                "content":
                    msg.content,

                "created_at":
                    msg.created_at

            }

            for msg in sorted(
                conversation.messages or [],
                key=lambda x:
                    x.created_at or datetime.min
            )

        ]

    }





# =====================================================
# AGENT SEND MESSAGE
# =====================================================

@router.post("/{conversation_id}/send")
def send_message(
    conversation_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):


    conversation = (

        db.query(models.Conversation)

        .filter(
            models.Conversation.id == conversation_id
        )

        .first()

    )


    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


    content = payload.get("content")


    if not content or not content.strip():

        raise HTTPException(
            status_code=400,
            detail="Message content required"
        )


    message = models.Message(

        conversation_id=conversation.id,

        role="agent",

        content=content.strip()

    )


    db.add(message)


    conversation.updated_at = datetime.now(
        timezone.utc
    )


    db.commit()

    db.refresh(message)


    return {

        "success": True,

        "message": {

            "id": message.id,

            "role": message.role,

            "content": message.content,

            "created_at":
                message.created_at

        }

    }





# =====================================================
# AI TOGGLE
# =====================================================

@router.patch("/{conversation_id}/ai")
def toggle_ai(
    conversation_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):

    conversation = (

        db.query(models.Conversation)

        .filter(
            models.Conversation.id == conversation_id
        )

        .first()

    )


    if not conversation:

        raise HTTPException(
            404,
            "Conversation not found"
        )


    conversation.is_ai_active = bool(
        payload.get(
            "is_ai_active"
        )
    )


    db.commit()


    return {

        "success": True,

        "is_ai_active":
            conversation.is_ai_active

    }





# =====================================================
# CLOSE CONVERSATION
# =====================================================

@router.patch("/{conversation_id}/close")
def close_conversation(
    conversation_id: int,
    db: Session = Depends(get_db)
):

    conversation = (

        db.query(models.Conversation)

        .filter(
            models.Conversation.id == conversation_id
        )

        .first()

    )


    if not conversation:

        raise HTTPException(
            404,
            "Conversation not found"
        )


    conversation.status = "closed"


    conversation.updated_at = datetime.now(
        timezone.utc
    )


    db.commit()


    return {

        "success": True,

        "status": "closed"

    }