import os
import logging
import asyncio

from dotenv import load_dotenv

from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


from app.database import SessionLocal
from app import models

from app.services.ai_service import generate_response


load_dotenv()


logging.basicConfig(
    level=logging.INFO
)


TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)



# =========================
# START COMMAND
# =========================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user


    keyboard = [
        [
            KeyboardButton(
                "📱 Share phone number",
                request_contact=True
            )
        ]
    ]


    markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


    await update.message.reply_text(
        f"""
Hello {user.first_name} 👋

Welcome to Rozita AI CRM.

Please share your phone number
to create your customer profile.
""",
        reply_markup=markup
    )



# =========================
# CREATE / GET LEAD
# =========================

def get_or_create_lead(
    db,
    user,
    chat_id
):

    lead = (
        db.query(models.Lead)
        .filter(
            models.Lead.telegram_chat_id == str(chat_id)
        )
        .first()
    )


    if not lead:

        lead = models.Lead(

            full_name=user.full_name,

            telegram_chat_id=str(chat_id),

            telegram_username=user.username,

            platform="telegram",

            status="new"

        )


        db.add(lead)

        db.commit()

        db.refresh(lead)


    return lead



# =========================
# CREATE / GET CONVERSATION
# =========================

def get_or_create_conversation(
    db,
    lead,
    chat_id
):

    conversation = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.lead_id == lead.id,
            models.Conversation.platform == "telegram"
        )
        .first()
    )


    if not conversation:


        conversation = models.Conversation(

            lead_id=lead.id,

            platform="telegram",

            platform_chat_id=str(chat_id),

            ai_enabled=True,

            status="open"

        )


        db.add(conversation)

        db.commit()

        db.refresh(conversation)


    return conversation



# =========================
# SAVE CONTACT
# =========================

async def save_contact(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    contact = update.message.contact


    db = SessionLocal()


    try:

        lead = (
            db.query(models.Lead)
            .filter(
                models.Lead.telegram_chat_id ==
                str(update.effective_chat.id)
            )
            .first()
        )


        if lead:

            lead.phone = contact.phone_number

            lead.full_name = contact.first_name


        else:

            lead = models.Lead(

                full_name=contact.first_name,

                phone=contact.phone_number,

                telegram_chat_id=
                str(update.effective_chat.id),

                platform="telegram"

            )


            db.add(lead)



        db.commit()


        await update.message.reply_text(
            """
Thank you ✅

Your phone number has been saved.

You can now ask your questions.
"""
        )


    except Exception as e:

        logging.error(
            f"Contact error: {e}"
        )


    finally:

        db.close()



# =========================
# MESSAGE HANDLER
# =========================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    text = update.message.text


    user = update.effective_user


    chat_id = update.effective_chat.id



    db = SessionLocal()



    try:


        # Lead
        lead = get_or_create_lead(
            db,
            user,
            chat_id
        )


        # Conversation
        conversation = get_or_create_conversation(
            db,
            lead,
            chat_id
        )



        # Save user message

        user_message = models.Message(

            conversation_id=conversation.id,

            role="user",

            content=text

        )


        db.add(user_message)

        db.commit()



        # AI Response

        response = await generate_response(
            text
        )



        # Save AI message

        ai_message = models.Message(

            conversation_id=conversation.id,

            role="assistant",

            content=response

        )


        db.add(ai_message)



        # update conversation time

        conversation.updated_at = models.datetime.utcnow()



        db.commit()



    except Exception as e:


        logging.error(
            f"Message error: {e}"
        )


        response = (
            "Sorry, something went wrong."
        )


    finally:

        db.close()



    await update.message.reply_text(
        response
    )



# =========================
# RUN BOT
# =========================

def run_bot():


    async def start_bot():


        application = (
            Application
            .builder()
            .token(TOKEN)
            .build()
        )



        application.add_handler(
            CommandHandler(
                "start",
                start
            )
        )



        application.add_handler(
            MessageHandler(
                filters.CONTACT,
                save_contact
            )
        )



        application.add_handler(
            MessageHandler(
                filters.TEXT &
                ~filters.COMMAND,
                handle_message
            )
        )



        print(
            "🤖 Telegram bot running..."
        )



        await application.initialize()


        await application.start()


        await application.updater.start_polling()



        await asyncio.Event().wait()



    asyncio.run(
        start_bot()
    )