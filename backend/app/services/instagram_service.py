import os
import requests
from sqlalchemy.orm import Session
from app import models
import logging

logger = logging.getLogger(__name__)

INSTAGRAM_API_URL = "https://graph.instagram.com/v18.0"

class InstagramService:
    def __init__(self):
        self.access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        self.business_account_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")

    async def get_messages(self, db: Session):
        """پیام‌های Instagram رو بگیر"""
        if not self.access_token:
            logger.warning("Instagram token not set")
            return []

        try:
            url = f"{INSTAGRAM_API_URL}/{self.business_account_id}/conversations"
            params = {
                "access_token": self.access_token,
                "fields": "id,senders,participants,snippet,updated_time"
            }
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            messages = []
            if "data" in data:
                for conv in data["data"]:
                    msg = {
                        "platform_id": conv.get("id"),
                        "platform": "instagram",
                        "sender": conv.get("senders", [{}])[0].get("name", "Unknown"),
                        "content": conv.get("snippet", ""),
                        "timestamp": conv.get("updated_time")
                    }
                    messages.append(msg)

            return messages
        except Exception as e:
            logger.error(f"Instagram error: {e}")
            return []

    async def send_message(self, conversation_id: str, message: str) -> bool:
        """پیام به Instagram بفرس"""
        if not self.access_token:
            return False

        try:
            url = f"{INSTAGRAM_API_URL}/{conversation_id}/messages"
            data = {
                "message": message,
                "access_token": self.access_token
            }
            response = requests.post(url, json=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Send message error: {e}")
            return False

    async def sync_to_crm(self, db: Session):
        """پیام‌های Instagram رو به CRM اضافه کن"""
        messages = await self.get_messages(db)

        for msg in messages:
            # لید رو پیدا کن یا بساز
            lead = db.query(models.Lead).filter(
                models.Lead.platform == "instagram"
            ).first()

            if not lead:
                lead = models.Lead(
                    platform=models.PlatformEnum.instagram,
                    full_name=msg.get("sender")
                )
                db.add(lead)
                db.flush()

            # مکالمه رو پیدا کن یا بساز
            conv = db.query(models.Conversation).filter(
                models.Conversation.platform_chat_id == msg.get("platform_id"),
                models.Conversation.platform == models.PlatformEnum.instagram
            ).first()

            if not conv:
                conv = models.Conversation(
                    lead_id=lead.id,
                    platform=models.PlatformEnum.instagram,
                    platform_chat_id=msg.get("platform_id")
                )
                db.add(conv)
                db.flush()

            # پیام رو اضافه کن
            db_msg = models.Message(
                conversation_id=conv.id,
                role="user",
                content=msg.get("content")
            )
            db.add(db_msg)

        db.commit()
        logger.info(f"Synced {len(messages)} Instagram messages")

instagram_service = InstagramService()
