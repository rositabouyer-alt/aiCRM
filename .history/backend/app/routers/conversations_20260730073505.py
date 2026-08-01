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
# Supports:
# - Search
# - Filtering by platform/status
# - Pagination
# =====================================================

@router.get("/")
def get_conversations(
    search: Optional[str] = None,
    platform: Optional[str] = None,
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
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

        messages = sorted(
            conversation.messages or [],
            key=lambda x: x.created_at or datetime.min
        )


        lead_data = None


        if conversation.lead:

            lead_data = {

                "id": conversation.lead.id,

                "full_name": conversation.lead.full_name,

                "phone": conversation.lead.phone,

                "email": getattr(
                    conversation.lead,
                    "email",
                    None
                ),

                "platform": (
                    conversation.lead.platform.value
                    if conversation.lead.platform
                    else None
                ),

                "status": (
                    conversation.lead.status.value
                    if conversation.lead.status
                    else None
                )

            }


        result.append({

            "id": conversation.id,


            "platform": (
                conversation.platform.value
                if conversation.platform
                else None
            ),


            "status": conversation.status,


            "is_ai_active": (
                conversation.is_ai_active
            ),


            "created_at": conversation.created_at,


            "updated_at": conversation.updated_at,


            "lead": lead_data,


            "messages_count": len(messages),


            "last_message": (
                messages[-1].content
                if messages
                else None
            ),


            "messages": [

                {

                    "id": message.id,

                    "role": message.role,

                    "content": message.content,

                    "created_at": message.created_at

                }

                for message in messages

            ]

        })


    return {

        "page": page,

        "limit": limit,

        "total": len(result),

        "conversations": result

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


    messages = sorted(
        conversation.messages or [],
        key=lambda x: x.created_at or datetime.min
    )


    return {


        "id": conversation.id,


        "platform": (

            conversation.platform.value

            if conversation.platform

            else None

        ),


        "status": conversation.status,


        "is_ai_active": conversation.is_ai_active,


        "created_at": conversation.created_at,


        "updated_at": conversation.updated_at,


        "lead": {


            "id": conversation.lead.id,


            "full_name": conversation.lead.full_name,


            "phone": conversation.lead.phone,


            "email": getattr(
                conversation.lead,
                "email",
                None
            ),


            "platform": (

                conversation.lead.platform.value

                if conversation.lead.platform

                else None

            )


        }

        if conversation.lead

        else None,


        "messages": [

            {

                "id": msg.id,

                "role": msg.role,

                "content": msg.content,

                "created_at": msg.created_at

            }

            for msg in messages

        ]

    }





# =====================================================
# SEND MESSAGE FROM CRM DASHBOARD
# Agent -> Customer
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


    if not content:

        raise HTTPException(

            status_code=400,

            detail="Message content required"

        )


    message = models.Message(

        conversation_id=conversation_id,

        role="agent",

        content=content

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


            "created_at": message.created_at

        }

    }





# =====================================================
# CREATE MESSAGE
# Used by:
# Telegram
# WhatsApp
# Instagram
# Website Chat
# Email integrations
# =====================================================

@router.post("/{conversation_id}/messages")
def create_message(

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


    if not content:

        raise HTTPException(

            status_code=400,

            detail="Content required"

        )



    role = payload.get(
        "role",
        "user"
    )


    allowed_roles = [

        "user",

        "agent",

        "assistant",

        "system"

    ]


    if role not in allowed_roles:

        raise HTTPException(

            status_code=400,

            detail="Invalid message role"

        )



    message = models.Message(

        conversation_id=conversation_id,

        role=role,

        content=content

    )


    db.add(message)



    conversation.updated_at = datetime.now(
        timezone.utc
    )


    db.commit()

    db.refresh(message)



    return {


        "id": message.id,


        "role": message.role,


        "content": message.content,


        "created_at": message.created_at

    }





# =====================================================
# TOGGLE AI ASSISTANT
# Enable / Disable AI for human takeover
# =====================================================

@router.patch("/{conversation_id}/ai-status")
def update_ai_status(

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



    ai_active = payload.get(
        "is_ai_active"
    )


    if ai_active is None:

        raise HTTPException(

            status_code=400,

            detail="is_ai_active required"

        )


    conversation.is_ai_active = bool(
        ai_active
    )


    conversation.updated_at = datetime.now(
        timezone.utc
    )


    db.commit()


    return {


        "success": True,


        "is_ai_active": conversation.is_ai_active

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

            status_code=404,

            detail="Conversation not found"

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