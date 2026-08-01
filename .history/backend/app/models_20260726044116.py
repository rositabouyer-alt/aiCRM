from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Enum, ForeignKey, Boolean
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

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200))
    phone = Column(String(20))
    age = Column(Integer, nullable=True)
    budget = Column(Float, nullable=True)
    preferred_contact_time = Column(String(100), nullable=True)
    needs = Column(Text, nullable=True)
    platform = Column(Enum(PlatformEnum), default=PlatformEnum.website)
    status = Column(Enum(LeadStatusEnum), default=LeadStatusEnum.new)
    telegram_chat_id = Column(String(100), nullable=True)
    ai_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    conversations = relationship("Conversation", back_populates="lead")
    bookings = relationship("Booking", back_populates="lead")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    platform = Column(Enum(PlatformEnum), default=PlatformEnum.website)
    platform_chat_id = Column(String(100), nullable=True)
    is_ai_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    lead = relationship("Lead", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String(20))  # user / assistant / admin
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    scheduled_at = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer, default=30)
    notes = Column(Text, nullable=True)
    status = Column(String(50), default="pending")  # pending / confirmed / cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lead = relationship("Lead", back_populates="bookings")
