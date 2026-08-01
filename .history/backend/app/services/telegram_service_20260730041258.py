import os
import asyncio
from datetime import datetime, timedelta

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

from app.database import SessionLocal
from app import models


load_dotenv()


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


NAME, PHONE, BOOKING = range(3)



# =========================
# Save message helper
# =========================

def save_message(
    chat_id: str,
    content: str,
    role: str = "user"
):

    db = SessionLocal()

    try:

        conversation = (
            db.query(models.Conversation)
            .filter(
                models.Conversation.platform_chat_id == chat_id
            )
            .first()
        )


        if conversation:

            db.add(
                models.Message(
                    conversation_id=conversation.id,
                    role=role,
                    content=content
                )
            )


            conversation.updated_at = datetime.now()


            db.commit()


    finally:

        db.close()




# =========================
# START
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat_id = str(
        update.effective_chat.id
    )


    save_message(
        chat_id,
        "/start",
        "user"
    )


    text = (
        "Hello 👋\n\n"
        "Welcome to Lumora AI CRM.\n\n"
        "Please send your name."
    )


    await update.message.reply_text(
        text
    )


    save_message(
        chat_id,
        text,
        "assistant"
    )


    return NAME




# =========================
# NAME
# =========================

async def get_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    name = update.message.text


    context.user_data["name"] = name



    save_message(
        str(update.effective_chat.id),
        name,
        "user"
    )



    keyboard = [
        [
            KeyboardButton(
                "📱 Send phone number",
                request_contact=True
            )
        ]
    ]



    text = "Please send your phone number."



    await update.message.reply_text(

        text,

        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )

    )


    save_message(
        str(update.effective_chat.id),
        text,
        "assistant"
    )


    return PHONE





# =========================
# PHONE
# =========================

async def get_phone(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    phone = update.message.contact.phone_number

    name = context.user_data.get(
        "name",
        "Unknown"
    )


    chat_id = str(
        update.effective_chat.id
    )


    save_message(
        chat_id,
        phone,
        "user"
    )



    db = SessionLocal()


    try:


        lead = (
            db.query(models.Lead)
            .filter(
                models.Lead.telegram_chat_id == chat_id
            )
            .first()
        )



        if not lead:


            lead = models.Lead(

                full_name=name,

                phone=phone,

                telegram_chat_id=chat_id,

                telegram_username=
                update.effective_user.username,

                platform="telegram"

            )


            db.add(lead)

            db.commit()

            db.refresh(lead)


        else:


            lead.full_name = name

            lead.phone = phone



        conversation = (
            db.query(models.Conversation)
            .filter(
                models.Conversation.lead_id == lead.id
            )
            .first()
        )



        if not conversation:


            conversation = models.Conversation(

                lead_id=lead.id,

                platform="telegram",

                platform_chat_id=chat_id,

                status="open",

                is_ai_active=True

            )


            db.add(conversation)

            db.commit()



        slots = get_available_slots(db)



    finally:

        db.close()





    keyboard = [
        [slot]
        for slot in slots
    ]



    text = (
        "✅ Your information saved.\n\n"
        "Please choose an available time:"
    )



    await update.message.reply_text(

        text,

        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

    )


    save_message(
        chat_id,
        text,
        "assistant"
    )



    return BOOKING





# =========================
# AVAILABLE SLOTS
# =========================

def get_available_slots(db):


    slots = []

    today = datetime.now()


    for i in range(7):

        day = today + timedelta(days=i)


        for hour in [10,12,14,16]:


            time = day.replace(
                hour=hour,
                minute=0,
                second=0,
                microsecond=0
            )



            exists = (
                db.query(models.Booking)
                .filter(
                    models.Booking.scheduled_at == time
                )
                .first()
            )



            if not exists:

                slots.append(
                    time.strftime(
                        "%Y-%m-%d %H:%M"
                    )
                )


    return slots[:10]





# =========================
# BOOKING
# =========================

async def create_booking(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    selected = update.message.text


    chat_id = str(
        update.effective_chat.id
    )


    save_message(
        chat_id,
        selected,
        "user"
    )



    db = SessionLocal()


    try:


        lead = (
            db.query(models.Lead)
            .filter(
                models.Lead.telegram_chat_id == chat_id
            )
            .first()
        )



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


        lead.status = "booked"



        conversation = (
            db.query(models.Conversation)
            .filter(
                models.Conversation.lead_id == lead.id
            )
            .first()
        )



        if conversation:


            conversation.updated_at = datetime.now()



        db.commit()



    finally:

        db.close()




    text = (
        "🎉 Booking confirmed!\n\n"
        f"Date: {selected}\n"
        "We will contact you soon."
    )



    await update.message.reply_text(
        text
    )



    save_message(
        chat_id,
        text,
        "assistant"
    )



    return ConversationHandler.END





# =========================
# RUN BOT
# =========================

async def start_bot():


    app = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )



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



    print(
        "🤖 Telegram bot running..."
    )



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