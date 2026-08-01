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


    id = Column(Integer, primary_key=True)


    full_name = Column(String(200), nullable=False)

    phone = Column(String(50), nullable=True)


    age = Column(Integer, nullable=True)

    budget = Column(Float, nullable=True)


    needs = Column(Text, nullable=True)


    platform = Column(
        Enum(PlatformEnum),
        default=PlatformEnum.telegram
    )


    status = Column(
        Enum(LeadStatusEnum),
        default=LeadStatusEnum.new
    )


    telegram_chat_id = Column(
        String(100),
        unique=True,
        nullable=True
    )


    telegram_username = Column(
        String(100),
        nullable=True
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
        onupdate=func.now()
    )


    conversations = relationship(
        "Conversation",
        back_populates="lead",
        cascade="all, delete"
    )


    bookings = relationship(
        "Booking",
        back_populates="lead",
        cascade="all, delete"
    )




# =====================
# CONVERSATION
# =====================

class Conversation(Base):

    __tablename__="conversations"


    id = Column(
        Integer,
        primary_key=True
    )


    lead_id = Column(
        Integer,
        ForeignKey("leads.id")
    )


    platform = Column(
        Enum(PlatformEnum),
        default=PlatformEnum.telegram
    )


    platform_chat_id = Column(
        String(100)
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
        server_default=func.now()
    )



    lead = relationship(
        "Lead",
        back_populates="conversations"
    )


    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete"
    )





# =====================
# MESSAGE
# =====================

class Message(Base):

    __tablename__="messages"


    id = Column(
        Integer,
        primary_key=True
    )


    conversation_id = Column(
        Integer,
        ForeignKey(
            "conversations.id"
        )
    )


    role = Column(
        String(20)
    )


    content = Column(
        Text
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

    __tablename__="bookings"


    id = Column(
        Integer,
        primary_key=True
    )


    lead_id = Column(
        Integer,
        ForeignKey(
            "leads.id"
        )
    )


    service = Column(
        String(255),
        nullable=True
    )


    scheduled_at = Column(
        DateTime(timezone=True)
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