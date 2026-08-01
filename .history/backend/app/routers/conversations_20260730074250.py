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
            joinedload(models.Conversation.lead)
            .joinedload(models.Lead.bookings),

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
            conversation.messages,
            key=lambda x: x.created_at or datetime.min
        )


        lead = conversation.lead


        bookings = []


        if lead:

            for booking in lead.bookings:

                bookings.append({

                    "id": booking.id,

                    "service": booking.service,

                    "scheduled_at": booking.scheduled_at,

                    "duration_minutes":
                        booking.duration_minutes,

                    "status": booking.status,

                    "notes": booking.notes,

                    "created_at": booking.created_at

                })



        result.append({

            "id": conversation.id,


            "platform": (
                conversation.platform.value
                if conversation.platform
                else None
            ),


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

                "full_name": lead.full_name,

                "phone": lead.phone,

                "email": lead.email,

                "telegram_username":
                    lead.telegram_username,

                "telegram_chat_id":
                    lead.telegram_chat_id,

                "whatsapp":
                    lead.whatsapp,

                "instagram":
                    lead.instagram,

                "status":
                    lead.status.value
                    if lead.status
                    else None,

                "needs":
                    lead.needs,

                "ai_summary":
                    lead.ai_summary

            }
            if lead else None,


            "bookings": bookings,


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

            joinedload(
                models.Conversation.lead
            )
            .joinedload(
                models.Lead.bookings
            ),


            joinedload(
                models.Conversation.messages
            )

        )

        .filter(
            models.Conversation.id ==
            conversation_id
        )

        .first()

    )


    if not conversation:

        raise HTTPException(
            404,
            "Conversation not found"
        )


    lead = conversation.lead


    return {

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


        "lead": {

            "id": lead.id,

            "full_name":
                lead.full_name,

            "phone":
                lead.phone,

            "email":
                lead.email

        },


        "bookings": [

            {

                "id": booking.id,

                "service":
                    booking.service,

                "scheduled_at":
                    booking.scheduled_at,

                "duration_minutes":
                    booking.duration_minutes,

                "status":
                    booking.status,

                "notes":
                    booking.notes

            }

            for booking in lead.bookings

        ],


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
                conversation.messages,
                key=lambda x:
                    x.created_at or datetime.min
            )

        ]

    }





# =====================================================
# SEND MESSAGE FROM DASHBOARD
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
            models.Conversation.id ==
            conversation_id
        )

        .first()

    )


    if not conversation:

        raise HTTPException(
            404,
            "Conversation not found"
        )


    content = payload.get("content")


    if not content:

        raise HTTPException(
            400,
            "Message content required"
        )


    message = models.Message(

        conversation_id=conversation.id,

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

            "created_at":
                message.created_at

        }

    }


# =====================================================
# SEND MESSAGE FROM DASHBOARD AGENT
# =====================================================

@router.post("/{conversation_id}/send")
def send_message(
    conversation_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):


    conversation = (

        db.query(models.Conversation)

        .options(
            joinedload(
                models.Conversation.lead
            )
        )

        .filter(
            models.Conversation.id ==
            conversation_id
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



    # Save agent message in database

    message = models.Message(

        conversation_id=conversation.id,

        role="agent",

        content=content

    )


    db.add(message)



    conversation.updated_at = datetime.now(
        timezone.utc
    )


    db.commit()

    db.refresh(message)



    # =====================================
    # SEND TO REAL PLATFORM
    # =====================================

    platform = conversation.platform


    lead = conversation.lead



    # Telegram

    if platform == models.PlatformEnum.telegram:

        # بعداً به telegram_service وصل می‌شود
        # send_telegram_message(
        #     chat_id=lead.telegram_chat_id,
        #     text=content
        # )

        pass



    # WhatsApp

    elif platform == models.PlatformEnum.whatsapp:

        # send_whatsapp_message(
        #     phone=lead.whatsapp,
        #     text=content
        # )

        pass



    # Instagram

    elif platform == models.PlatformEnum.instagram:

        pass



    # Website Live Chat

    elif platform == models.PlatformEnum.website:

        pass



    return {


        "success": True,


        "sent": True,


        "message": {


            "id": message.id,


            "role": message.role,


            "content": message.content,


            "created_at": message.created_at

        }

    }


# =====================================================
# AI ON/OFF
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
            models.Conversation.id ==
            conversation_id
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
            models.Conversation.id ==
            conversation_id
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