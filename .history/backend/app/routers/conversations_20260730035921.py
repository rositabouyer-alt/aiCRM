from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timezone

from app.database import get_db
from app import models


router = APIRouter(
    prefix="/conversations",
    tags=["conversations"]
)



# ==========================
# Get all conversations
# ==========================

@router.get("/")
def get_conversations(
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
        .all()
    )


    result = []


    for conversation in conversations:


        messages = sorted(
            conversation.messages,
            key=lambda x: x.created_at
        )


        result.append({

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

                "platform": (
                    conversation.lead.platform.value
                    if conversation.lead.platform
                    else None
                ),

                "status": conversation.lead.status.value
                if conversation.lead.status
                else None

            }
            if conversation.lead
            else None,



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


    return result





# ==========================
# Get single conversation
# ==========================

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



    return {

        "id": conversation.id,


        "platform": (
            conversation.platform.value
            if conversation.platform
            else None
        ),


        "status": conversation.status,


        "is_ai_active": conversation.is_ai_active,


        "lead": {

            "id": conversation.lead.id,

            "full_name": conversation.lead.full_name,

            "phone": conversation.lead.phone,

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

                "id": message.id,

                "role": message.role,

                "content": message.content,

                "created_at": message.created_at

            }

            for message in sorted(
                conversation.messages,
                key=lambda x:x.created_at
            )

        ]

    }





# ==========================
# Create message
# ==========================

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



    content = payload.get(
        "content"
    )


    if not content:

        raise HTTPException(
            status_code=400,
            detail="Message content required"
        )



    message = models.Message(

        conversation_id=conversation_id,

        role=payload.get(
            "role",
            "user"
        ),

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