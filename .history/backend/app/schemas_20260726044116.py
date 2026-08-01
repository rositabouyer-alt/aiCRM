from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models import PlatformEnum, LeadStatusEnum

# ---- Lead ----
class LeadCreate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    budget: Optional[float] = None
    preferred_contact_time: Optional[str] = None
    needs: Optional[str] = None
    platform: PlatformEnum = PlatformEnum.website
    telegram_chat_id: Optional[str] = None

class LeadUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    budget: Optional[float] = None
    status: Optional[LeadStatusEnum] = None
    needs: Optional[str] = None
    ai_summary: Optional[str] = None

class LeadOut(BaseModel):
    id: int
    full_name: Optional[str]
    phone: Optional[str]
    age: Optional[int]
    budget: Optional[float]
    platform: PlatformEnum
    status: LeadStatusEnum
    ai_summary: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# ---- Message ----
class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

# ---- Conversation ----
class ConversationOut(BaseModel):
    id: int
    platform: PlatformEnum
    is_ai_active: bool
    lead: Optional[LeadOut]
    messages: List[MessageOut] = []
    created_at: datetime

    class Config:
        from_attributes = True

# ---- Booking ----
class BookingCreate(BaseModel):
    lead_id: int
    scheduled_at: datetime
    duration_minutes: int = 30
    notes: Optional[str] = None

class BookingOut(BaseModel):
    id: int
    lead_id: int
    scheduled_at: datetime
    duration_minutes: int
    status: str
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# ---- Chat (برای دشبورد) ----
class SendMessageRequest(BaseModel):
    conversation_id: int
    content: str
