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

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


logging.basicConfig(
    level=logging.INFO
)


# ==========================
# Create or Get Lead
# ==========================

def get_or_create_lead(db, user, chat_id):

    lead = db.query(models.Lead).filter(
        models.Lead.telegram_chat_id == str(chat_id)
    ).first()


    if not lead:

        lead = models.Lead(
            full_name=user.full_name,
            telegram_username=user.username,
            telegram_chat_id=str(chat_id),
            platform="telegram"
        )

        db.add(lead)
        db.commit()
        db.refresh(lead)


    return lead



# ==========================
# Create or Get Conversation
# ==========================

def get_or_create_conversation(db, lead, chat_id):

    conversation = db.query(
        models.Conversation
    ).filter(
        models.Conversation.platform_chat_id == str(chat_id)
    ).first()


    if not conversation:

        conversation = models.Conversation(
            lead_id=lead.id,
            platform="telegram",
            platform_chat_id=str(chat_id),
            is_ai_active=True
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)


    return conversation




# ==========================
# START
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user


    keyboard = [
        [
            KeyboardButton(
                "📱 Send phone number",
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

Welcome to Lumora AI CRM.

Please send your phone number to continue.
""",
        reply_markup=markup
    )




# ==========================
# CONTACT
# ==========================

async def save_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):

    contact = update.message.contact

    db = SessionLocal()


    try:

        lead = db.query(models.Lead).filter(
            models.Lead.telegram_chat_id ==
            str(update.effective_chat.id)
        ).first()


        if lead:

            lead.phone = contact.phone_number
            lead.full_name = contact.first_name


        else:

            lead = models.Lead(
                full_name=contact.first_name,
                phone=contact.phone_number,
                telegram_chat_id=str(update.effective_chat.id),
                platform="telegram"
            )

            db.add(lead)


        db.commit()


        await update.message.reply_text(
            "✅ Your phone number has been saved.\nYou can ask your questions now."
        )


    except Exception as e:

        print("Contact error:", e)


    finally:

        db.close()





# ==========================
# TEXT MESSAGE
# ==========================

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

        conversation.updated_at = func.now()

        db.commit()



        # AI

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


        conversation.updated_at = func.now()


        db.commit()



        await update.message.reply_text(
            response
        )


    except Exception as e:

        print(
            "Message error:",
            e
        )


        await update.message.reply_text(
            "Sorry, something went wrong."
        )


    finally:

        db.close()




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


        print("🤖 Telegram bot running...")


        await app.initialize()

        await app.start()

        await app.updater.start_polling()


        await asyncio.Event().wait()



    asyncio.run(start_bot())