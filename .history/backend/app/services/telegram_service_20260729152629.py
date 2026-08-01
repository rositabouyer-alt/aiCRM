import os
import logging
import asyncio
from sqlalchemy.sql import func
from dotenv import load_dotenv

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models

import os


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


NAME, PHONE, BOOKING = range(3)


# -------------------------
# Database helper
# -------------------------

def get_db():
    db = SessionLocal()
    try:
        return db
    except:
        db.close()



# -------------------------
# START
# -------------------------

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "Hello 👋\n\n"
        "Welcome to Lumora AI CRM.\n\n"
        "Please send your name."
    )

    return NAME



# -------------------------
# NAME
# -------------------------

async def get_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data["name"] = update.message.text


    keyboard = [
        [
            KeyboardButton(
                "📱 Send phone number",
                request_contact=True
            )
        ]
    ]


    await update.message.reply_text(
        "Please send your phone number.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


    return PHONE




# -------------------------
# PHONE
# -------------------------

async def get_phone(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    phone = update.message.contact.phone_number

    name = context.user_data["name"]


    db = SessionLocal()


    lead = db.query(
        models.Lead
    ).filter(
        models.Lead.telegram_chat_id ==
        str(update.effective_chat.id)
    ).first()



    if not lead:

        lead = models.Lead(

            full_name=name,

            phone=phone,

            telegram_chat_id=
            str(update.effective_chat.id),

            telegram_username=
            update.effective_user.username,

            platform="telegram"

        )


        db.add(lead)


    else:

        lead.phone = phone
        lead.full_name = name



    db.commit()
    db.refresh(lead)



    # conversation

    conversation = db.query(
        models.Conversation
    ).filter(
        models.Conversation.lead_id == lead.id
    ).first()



    if not conversation:

        conversation = models.Conversation(

            lead_id=lead.id,

            platform="telegram",

            platform_chat_id=
            str(update.effective_chat.id)

        )

        db.add(conversation)

        db.commit()



    # show available slots

    slots = get_available_slots(db)



    keyboard = [
        [slot]
        for slot in slots
    ]


    await update.message.reply_text(

        "✅ Your information saved.\n\n"
        "Please choose an available time:",

        reply_markup=
        ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

    )


    return BOOKING




# -------------------------
# AVAILABLE TIMES
# -------------------------

def get_available_slots(db):

    today = datetime.now()


    slots = []


    for i in range(7):

        day = today + timedelta(days=i)


        for hour in [10,12,14,16]:

            time = day.replace(
                hour=hour,
                minute=0,
                second=0
            )


            exists = db.query(
                models.Booking
            ).filter(
                models.Booking.scheduled_at
                ==
                time
            ).first()



            if not exists:

                slots.append(
                    time.strftime(
                        "%Y-%m-%d %H:%M"
                    )
                )


    return slots[:10]





# -------------------------
# CREATE BOOKING
# -------------------------

async def create_booking(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE

):

    selected = update.message.text


    db = SessionLocal()



    lead = db.query(
        models.Lead
    ).filter(
        models.Lead.telegram_chat_id ==
        str(update.effective_chat.id)
    ).first()



    if not lead:

        await update.message.reply_text(
            "Please restart."
        )

        return ConversationHandler.END




    booking = models.Booking(

        lead_id=lead.id,

        service="AI Consultation",

        scheduled_at=datetime.strptime(

            selected,

            "%Y-%m-%d %H:%M"

        ),

        duration_minutes=30,

        status="confirmed"

    )


    db.add(booking)


    lead.status="booked"



    conversation = db.query(
        models.Conversation
    ).filter(
        models.Conversation.lead_id==lead.id
    ).first()



    if conversation:

        message = models.Message(

            conversation_id=
            conversation.id,

            role="user",

            content=
            f"Booking selected: {selected}"

        )


        db.add(message)


        conversation.updated_at=datetime.now()



    db.commit()



    await update.message.reply_text(

        "🎉 Booking confirmed!\n\n"

        f"Date: {selected}\n"

        "We will contact you soon."

    )



    return ConversationHandler.END





# -------------------------
# RUN BOT
# -------------------------

async def start_bot():

    app = Application.builder().token(
        BOT_TOKEN
    ).build()


    conv = ConversationHandler(

        entry_points=[
            CommandHandler(
                "start",
                start
            )
        ],


        states={

            NAME:[
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_name
                )
            ],


            PHONE:[
                MessageHandler(
                    filters.CONTACT,
                    get_phone
                )
            ],


            BOOKING:[
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    create_booking
                )
            ]

        },


        fallbacks=[]

    )


    app.add_handler(conv)


    print("🤖 Telegram bot running...")


    await app.initialize()
    await app.start()
    await app.updater.start_polling()


    await asyncio.Event().wait()



def run_bot():

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)


    try:

        loop.run_until_complete(
            start_bot()
        )

    finally:

        loop.close()