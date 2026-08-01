import os
import asyncio
import logging

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

from sqlalchemy.sql import func

from app.database import SessionLocal
from app import models

from app.services.ai_service import generate_response


load_dotenv()

logging.basicConfig(
    level=logging.INFO
)


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# ==========================
# START COMMAND
# ==========================

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

Please share your phone number so we can assist you better.
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

        chat_id = str(update.effective_chat.id)


        lead = db.query(
            models.Lead
        ).filter(
            models.Lead.telegram_chat_id == chat_id
        ).first()



        if lead:

            lead.phone = contact.phone_number
            lead.full_name = contact.first_name

        else:

            lead = models.Lead(
                full_name=contact.first_name,
                phone=contact.phone_number,
                telegram_chat_id=chat_id,
                platform=models.PlatformEnum.telegram,
                status=models.LeadStatusEnum.new
            )

            db.add(lead)


        db.commit()



        await update.message.reply_text(
            """
✅ Your phone number has been saved.

You can now send your questions.
"""
        )


    except Exception as e:

        print(
            "Contact error:",
            e
        )


    finally:

        db.close()



# ==========================
# HANDLE ALL TEXT MESSAGES
# ==========================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text

    user = update.effective_user

    chat_id = str(
        update.effective_chat.id
    )


    db = SessionLocal()


    try:


        # ----------------------
        # Find or create Lead
        # ----------------------

        lead = db.query(
            models.Lead
        ).filter(
            models.Lead.telegram_chat_id == chat_id
        ).first()



        if not lead:


            lead = models.Lead(
                full_name=user.full_name,
                telegram_chat_id=chat_id,
                platform=models.PlatformEnum.telegram,
                status=models.LeadStatusEnum.new
            )


            db.add(lead)

            db.commit()

            db.refresh(lead)




        # ----------------------
        # Find or create Conversation
        # ----------------------

        conversation = db.query(
            models.Conversation
        ).filter(
            models.Conversation.lead_id == lead.id
        ).first()



        if not conversation:


            conversation = models.Conversation(
                lead_id=lead.id,
                platform=models.PlatformEnum.telegram,
                platform_chat_id=chat_id,
                is_ai_active=True
            )


            db.add(conversation)

            db.commit()

            db.refresh(conversation)




        # ----------------------
        # Save User Message
        # ----------------------

        user_message = models.Message(

            conversation_id=conversation.id,

            role="user",

            content=text
        )


        db.add(user_message)

        db.commit()



        # ----------------------
        # AI Response
        # ----------------------

        response = await generate_response(
            text,
            {
                "name": lead.full_name,
                "phone": lead.phone
            }
        )



        # ----------------------
        # Save AI Message
        # ----------------------

        ai_message = models.Message(

            conversation_id=conversation.id,

            role="assistant",

            content=response
        )


        db.add(ai_message)



        conversation.updated_at = func.now()


        db.commit()



    except Exception as e:


        print(
            "Telegram message error:",
            e
        )


        response = (
            "Sorry, an error happened. "
            "Please try again."
        )


    finally:

        db.close()



    await update.message.reply_text(
        response
    )



# ==========================
# RUN BOT
# ==========================

def run_bot():


    async def start_bot():


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
            MessageHandler(
                filters.CONTACT,
                save_contact
            )
        )



        app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
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



    asyncio.run(start_bot())