from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.models import PlatformEnum, LeadStatusEnum



# =====================
# LEAD
# =====================

class LeadCreate(BaseModel):

    full_name: str

    phone: Optional[str] = None

    age: Optional[int] = None

    budget: Optional[float] = None

    needs: Optional[str] = None

    platform: PlatformEnum = PlatformEnum.website

    telegram_chat_id: Optional[int] = None

    telegram_username: Optional[str] = None



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

    full_name: Optional[str] = None

    phone: Optional[str] = None

    telegram_username: Optional[str] = None

    telegram_chat_id: Optional[int] = None

    age: Optional[int] = None

    budget: Optional[float] = None

    platform: PlatformEnum

    status: LeadStatusEnum

    ai_summary: Optional[str] = None

    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None



    class Config:

        from_attributes = True




# =====================
# MESSAGE
# =====================

class MessageOut(BaseModel):

    id: int

    role: str

    content: str

    created_at: Optional[datetime] = None



    class Config:

        from_attributes = True




# =====================
# CONVERSATION
# =====================

class ConversationOut(BaseModel):

    id: int

    platform: PlatformEnum

    platform_chat_id: Optional[str] = None

    is_ai_active: bool

    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None


    lead: Optional[LeadOut] = None


    messages: List[MessageOut] = []



    class Config:

        from_attributes = True




# =====================
# BOOKING
# =====================

class BookingCreate(BaseModel):

    lead_id: int

    service: Optional[str] = "AI Consultation"

    scheduled_at: datetime

    duration_minutes: int = 30

    status: Optional[str] = "pending"

    notes: Optional[str] = None




class BookingOut(BaseModel):

    id: int

    lead_id: int

    service: Optional[str] = None

    scheduled_at: datetime

    duration_minutes: int

    status: str

    notes: Optional[str] = None

    created_at: Optional[datetime] = None



    class Config:

        from_attributes = True




# =====================
# SEND MESSAGE
# =====================

class SendMessageRequest(BaseModel):

    content: str