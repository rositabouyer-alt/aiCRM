import os
import requests
from sqlalchemy.orm import Session
from app import models
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")

    async def get_messages(self, db: Session):
        """پیام‌های WhatsApp رو بگیر"""
        # وقتی API فعال شد، اینجا پیام‌ها رو می‌گیریم
        return []

    async def send_message(self, phone: str, message: str) -> bool:
        """پیام به WhatsApp بفرس"""
        if not self.access_token:
            logger.warning("WhatsApp token not set")
            return False
        
        # بعداً پیاده‌سازی می‌کنیم
        return False

whatsapp_service = WhatsAppService()
