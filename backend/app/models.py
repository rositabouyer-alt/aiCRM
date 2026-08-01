from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Float,
    Enum,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

import enum


# =====================
# ENUMS
# =====================

class PlatformEnum(str, enum.Enum):
    telegram = "telegram"
    website = "website"
    whatsapp = "whatsapp"
    instagram = "instagram"
    direct = "direct"


class LeadStatusEnum(str, enum.Enum):
    new = "new"
    active = "active"
    qualified = "qualified"
    booked = "booked"
    closed = "closed"



# =====================
# LEAD
# =====================

class Lead(Base):

    __tablename__ = "leads"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    full_name = Column(
        String(255),
        nullable=True
    )


    phone = Column(
        String(20),
        nullable=True
    )


    email = Column(
        String(255),
        nullable=True
    )


    telegram_id = Column(
        String(100),
        nullable=True
    )


    telegram_username = Column(
        String(100),
        nullable=True
    )


    telegram_chat_id = Column(
        String(100),
        nullable=True,
        unique=True
    )


    whatsapp = Column(
        String(20),
        nullable=True
    )


    instagram = Column(
        String(100),
        nullable=True
    )


    age = Column(
        Integer,
        nullable=True
    )


    budget = Column(
        Float,
        nullable=True
    )


    needs = Column(
        Text,
        nullable=True
    )


    platform = Column(
        Enum(PlatformEnum),
        default=PlatformEnum.telegram
    )


    status = Column(
        Enum(LeadStatusEnum),
        default=LeadStatusEnum.new
    )


    ai_summary = Column(
        Text,
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


    conversations = relationship(
        "Conversation",
        back_populates="lead",
        cascade="all, delete-orphan"
    )


    bookings = relationship(
        "Booking",
        back_populates="lead",
        cascade="all, delete-orphan"
    )



# =====================
# CONVERSATION
# =====================

class Conversation(Base):

    __tablename__ = "conversations"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        nullable=False
    )


    platform = Column(
        Enum(PlatformEnum),
        default=PlatformEnum.telegram
    )


    platform_chat_id = Column(
        String(100),
        nullable=True
    )


    status = Column(
        String(50),
        default="open"
    )


    is_ai_active = Column(
        Boolean,
        default=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


    lead = relationship(
        "Lead",
        back_populates="conversations"
    )


    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )



# =====================
# MESSAGE
# =====================

class Message(Base):

    __tablename__ = "messages"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=False
    )


    role = Column(
        String(20),
        nullable=False
    )


    content = Column(
        Text,
        nullable=False
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )



# =====================
# BOOKING
# =====================

class Booking(Base):

    __tablename__ = "bookings"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        nullable=False
    )


    service = Column(
        String(255),
        nullable=True
    )


    scheduled_at = Column(
        DateTime(timezone=True),
        nullable=False
    )


    duration_minutes = Column(
        Integer,
        default=30
    )


    status = Column(
        String(50),
        default="pending"
    )


    notes = Column(
        Text,
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    lead = relationship(
        "Lead",
        back_populates="bookings"
    )



class CallStatusEnum(str, enum.Enum):
    
    pending = "pending"
    completed = "completed"



class Call(Base):

    __tablename__ = "calls"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    lead_id = Column(
        Integer,
        ForeignKey("leads.id"),
        nullable=False
    )


    phone = Column(
        String(20),
        nullable=False
    )


    status = Column(
        Enum(CallStatusEnum),
        default=CallStatusEnum.pending
    )


    has_previous_conversation = Column(
        Boolean,
        default=False
    )


    notes = Column(
        Text,
        nullable=True
    )


    called_at = Column(
        DateTime(timezone=True),
        nullable=True
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    lead = relationship(
        "Lead"
    )