import os
import asyncio

from datetime import datetime, timedelta, timezone

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


BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)



NAME, PHONE, BOOKING = range(3)





# =====================================================
# SAVE MESSAGE + CREATE CRM DATA
# =====================================================

def save_message(
    chat_id: str,
    content: str,
    role: str = "user"
):

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

                telegram_chat_id=chat_id,

                platform=models.PlatformEnum.telegram,

                status=models.LeadStatusEnum.new

            )


            db.add(lead)

            db.commit()

            db.refresh(lead)





        conversation = (

            db.query(models.Conversation)

            .filter(

                models.Conversation.platform_chat_id
                == chat_id

            )

            .first()

        )




        if not conversation:


            conversation = models.Conversation(

                lead_id=lead.id,

                platform=models.PlatformEnum.telegram,

                platform_chat_id=chat_id,

                status="open",

                is_ai_active=True

            )


            db.add(conversation)

            db.commit()

            db.refresh(conversation)





        message = models.Message(

            conversation_id=conversation.id,

            role=role,

            content=content

        )


        db.add(message)



        conversation.updated_at = datetime.now(
            timezone.utc
        )



        db.commit()



    except Exception as e:


        db.rollback()

        print(
            "SAVE MESSAGE ERROR:",
            e
        )



    finally:

        db.close()





# =====================================================
# START
# =====================================================


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





# =====================================================
# NAME
# =====================================================


async def get_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    chat_id = str(
        update.effective_chat.id
    )


    name = update.message.text



    context.user_data["name"] = name



    save_message(
        chat_id,
        name,
        "user"
    )




    db = SessionLocal()


    try:


        lead = (

            db.query(models.Lead)

            .filter(
                models.Lead.telegram_chat_id
                == chat_id
            )

            .first()

        )


        if lead:

            lead.full_name = name


            db.commit()



    finally:

        db.close()






    keyboard = [

        [

            KeyboardButton(

                "Send phone number",

                request_contact=True

            )

        ]

    ]



    text = (
        "Please send your phone number."
    )



    await update.message.reply_text(

        text,

        reply_markup=ReplyKeyboardMarkup(

            keyboard,

            resize_keyboard=True,

            one_time_keyboard=True

        )

    )



    save_message(
        chat_id,
        text,
        "assistant"
    )



    return PHONE







# =====================================================
# PHONE
# =====================================================


async def get_phone(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    chat_id = str(
        update.effective_chat.id
    )


    phone = (
        update.message.contact.phone_number
    )


    name = context.user_data.get(
        "name",
        "Unknown"
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

                models.Lead.telegram_chat_id
                == chat_id

            )

            .first()

        )



        lead.full_name = name

        lead.phone = phone

        lead.telegram_username = (

            update.effective_user.username

        )



        db.commit()



        slots = get_available_slots(
            db
        )



    finally:

        db.close()




    keyboard = [

        [slot]

        for slot in slots

    ]



    text = (

        "Information saved successfully.\n\n"

        "Choose your appointment time:"

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







# =====================================================
# SLOTS
# =====================================================


def get_available_slots(db):


    slots = []

    now = datetime.now()



    for i in range(7):


        day = now + timedelta(
            days=i
        )


        for hour in [
            10,
            12,
            14,
            16
        ]:


            time = day.replace(

                hour=hour,

                minute=0,

                second=0,

                microsecond=0

            )



            exists = (

                db.query(models.Booking)

                .filter(

                    models.Booking.scheduled_at
                    == time

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







# =====================================================
# BOOKING
# =====================================================


async def create_booking(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    chat_id = str(
        update.effective_chat.id
    )


    selected = update.message.text



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

                models.Lead.telegram_chat_id
                == chat_id

            )

            .first()

        )



        if not lead:


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



        lead.status = models.LeadStatusEnum.booked



        db.commit()



    finally:

        db.close()





    text = (

        "Booking confirmed ✅\n\n"

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







# =====================================================
# GENERAL CUSTOMER MESSAGE
# =====================================================

async def general_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat_id = str(
        update.effective_chat.id
    )

    user_text = update.message.text.lower()


    # Save customer message
    save_message(
        chat_id,
        update.message.text,
        "user"
    )


    # ===============================
    # SMART RESPONSE
    # ===============================

    if any(word in user_text for word in [
        "hello",
        "hi",
        "hey"
    ]):

        reply = (
            "Hello 👋\n\n"
            "Welcome back to Lumora AI CRM.\n"
            "How can I help you today?"
        )


    elif any(word in user_text for word in [
        "price",
        "pricing",
        "cost"
    ]):

        reply = (
            "Our pricing depends on your requirements.\n\n"
            "Please tell me what service you need "
            "and our team will provide the best offer."
        )


    elif any(word in user_text for word in [
        "service",
        "services",
        "what do you do"
    ]):

        reply = (
            "Our services include:\n\n"
            "✅ AI CRM solutions\n"
            "✅ Customer automation\n"
            "✅ Telegram integration\n"
            "✅ Business workflow automation\n"
            "✅ AI assistants\n\n"
            "Tell me what you need help with."
        )


    elif any(word in user_text for word in [
        "appointment",
        "meeting",
        "call",
        "booking"
    ]):

        reply = (
            "Sure 👍\n\n"
            "You can schedule a consultation "
            "with our team.\n\n"
            "Please tell me your preferred time."
        )


    elif any(word in user_text for word in [
        "thank",
        "thanks"
    ]):

        reply = (
            "You're welcome 😊\n\n"
            "Feel free to ask anything else."
        )


    else:

        reply = (
            "Thank you for your message 🙏\n\n"
            "I received your request.\n"
            "Could you please provide more details "
            "so I can assist you better?"
        )



    await update.message.reply_text(
        reply
    )


    # Save bot response
    save_message(
        chat_id,
        reply,
        "assistant"
    )

# =====================================================
# RUN BOT
# =====================================================


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

                    filters.TEXT
                    &
                    ~filters.COMMAND,

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

                    filters.TEXT
                    &
                    ~filters.COMMAND,

                    create_booking

                )

            ]


        },



        fallbacks=[]

    )




    app.add_handler(conv)



    app.add_handler(

        MessageHandler(

            filters.TEXT
            &
            ~filters.COMMAND,

            general_message

        )

    )




    print(
        "Telegram bot running..."
    )



    await app.initialize()

    await app.start()

    await app.updater.start_polling()



    await asyncio.Event().wait()






def run_bot():


    loop = asyncio.new_event_loop()


    asyncio.set_event_loop(
        loop
    )


    loop.run_until_complete(
        start_bot()
    )