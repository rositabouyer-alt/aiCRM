import os
import asyncio
import logging

from dotenv import load_dotenv

from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from app.database import SessionLocal
from app import models
from app.services.ai_service import generate_response


load_dotenv()

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# ==========================
# START
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    keyboard = [
        [
            KeyboardButton(
                "📱 Send Phone Number",
                request_contact=True
            )
        ]
    ]

    markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


    await update.message.reply_text(
        f"""
Hello {user.first_name} 👋

Welcome to Rozita AI CRM.

Please send your phone number.
""",
        reply_markup=markup
    )



# ==========================
# SAVE CONTACT
# ==========================

async def save_contact(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    contact = update.message.contact

    db = SessionLocal()

    try:

        telegram_id = str(update.effective_user.id)


        lead = db.query(
            models.Lead
        ).filter(
            models.Lead.telegram_id == telegram_id
        ).first()


        if lead:

            lead.phone = contact.phone_number
            lead.full_name = contact.first_name

        else:

            lead = models.Lead(

                full_name=contact.first_name,

                phone=contact.phone_number,

                telegram_id=telegram_id,

                telegram_username=
                update.effective_user.username,

                platform="telegram",

                status="new"
            )

            db.add(lead)


        db.commit()


    finally:

        db.close()



    await update.message.reply_text(
        "✅ Your contact has been saved."
    )



# ==========================
# BOOKING START
# ==========================

async def booking_start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):


    keyboard = [

        [
            InlineKeyboardButton(
                "SEO Consultation",
                callback_data="service:SEO Consultation"
            )
        ],

        [
            InlineKeyboardButton(
                "Google Ads",
                callback_data="service:Google Ads"
            )
        ],

        [
            InlineKeyboardButton(
                "Landing Design",
                callback_data="service:Landing Design"
            )
        ]

    ]


    await update.message.reply_text(

        "Choose your service:",

        reply_markup=
        InlineKeyboardMarkup(keyboard)

    )




async def choose_service(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()


    service = query.data.split(":")[1]


    context.user_data["service"] = service


    keyboard=[

        [
            InlineKeyboardButton(
                "Tomorrow 10:00",
                callback_data="time:Tomorrow 10:00"
            )
        ],

        [
            InlineKeyboardButton(
                "Sunday 14:00",
                callback_data="time:Sunday 14:00"
            )
        ]

    ]


    await query.edit_message_text(

        "Choose appointment time:",

        reply_markup=
        InlineKeyboardMarkup(keyboard)

    )




async def save_booking(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):


    query = update.callback_query

    await query.answer()


    time = query.data.split(":")[1]


    service = context.user_data.get(
        "service"
    )


    db = SessionLocal()


    try:

        user = update.effective_user


        lead = db.query(
            models.Lead
        ).filter(
            models.Lead.telegram_id ==
            str(user.id)
        ).first()



        if not lead:

            lead=models.Lead(

                full_name=user.full_name,

                telegram_id=str(user.id),

                telegram_username=user.username,

                platform="telegram",

                status="new"
            )

            db.add(lead)

            db.flush()



        appointment=models.Appointment(

            lead_id=lead.id,

            title=service,

            scheduled_at=time,

            duration_minutes=30,

            status="scheduled"

        )


        db.add(appointment)

        db.commit()


    finally:

        db.close()



    await query.edit_message_text(

        f"""
✅ Booking Created

Service:
{service}

Time:
{time}
"""
    )



# ==========================
# NORMAL MESSAGE + AI
# ==========================

async def handle_message(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    user = update.effective_user


    db = SessionLocal()


    try:


        lead = db.query(
            models.Lead
        ).filter(
            models.Lead.telegram_id ==
            str(user.id)
        ).first()



        if not lead:


            lead=models.Lead(

                full_name=user.full_name,

                telegram_id=str(user.id),

                telegram_username=user.username,

                platform="telegram",

                status="new"

            )


            db.add(lead)

            db.flush()



        message=models.Message(

            lead_id=lead.id,

            role="user",

            content=text

        )


        db.add(message)

        db.commit()



        response = await generate_response(
            text
        )



        bot_message=models.Message(

            lead_id=lead.id,

            role="assistant",

            content=response

        )


        db.add(bot_message)

        db.commit()



    finally:

        db.close()



    await update.message.reply_text(
        response
    )



# ==========================
# BOT RUNNER
# ==========================

def run_bot():


    async def main():


        app = Application.builder() \
            .token(TOKEN) \
            .build()



        app.add_handler(
            CommandHandler(
                "start",
                start
            )
        )


        app.add_handler(
            CommandHandler(
                "booking",
                booking_start
            )
        )


        app.add_handler(
            MessageHandler(
                filters.CONTACT,
                save_contact
            )
        )


        app.add_handler(
            CallbackQueryHandler(
                choose_service,
                pattern="^service:"
            )
        )


        app.add_handler(
            CallbackQueryHandler(
                save_booking,
                pattern="^time:"
            )
        )


        app.add_handler(
            MessageHandler(
                filters.TEXT &
                ~filters.COMMAND,
                handle_message
            )
        )



        print(
            "🤖 Telegram bot running..."
        )


        await app.initialize()

        await app.start()

        await app.updater.start_polling()


        await asyncio.Event().wait()



    asyncio.run(main())