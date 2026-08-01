import os
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


from app.database import SessionLocal
from app import models

from app.services.ai_service import generate_response


load_dotenv()


logging.basicConfig(
    level=logging.INFO
)


from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# --------------------------
# Start
# --------------------------

async def start(
        update:Update,
        context:ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user


    keyboard=[
        [
            KeyboardButton(
                "📱 ارسال شماره تماس",
                request_contact=True
            )
        ]
    ]


    markup=ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


    await update.message.reply_text(
        f"""
سلام {user.first_name} 👋

به Lumora خوش آمدید.

برای ارتباط بهتر لطفا شماره تماس خود را ارسال کنید.
""",
        reply_markup=markup
    )



# --------------------------
# Contact Handler
# --------------------------


async def contact_handler(
        update:Update,
        context:ContextTypes.DEFAULT_TYPE
):

    contact=update.message.contact


    phone=contact.phone_number


    db=SessionLocal()


    lead=models.Lead(
        full_name=
        contact.first_name or "Unknown",

        phone=phone,

        platform="telegram",

        telegram_chat_id=
        str(update.effective_chat.id)
    )


    db.add(lead)

    db.commit()

    db.close()


    await update.message.reply_text(
        """
ممنون 🙏
شماره شما ثبت شد.

حالا سوال خود را بپرسید.
"""
    )





# --------------------------
# Message Handler
# --------------------------


async def message_handler(
        update:Update,
        context:ContextTypes.DEFAULT_TYPE
):


    text=update.message.text

    chat_id=str(
        update.effective_chat.id
    )


    db=SessionLocal()



    lead=db.query(
        models.Lead
    ).filter(
        models.Lead.telegram_chat_id==chat_id
    ).first()



    if not lead:

        lead=models.Lead(
            full_name=
            update.effective_user.first_name,

            telegram_chat_id=chat_id,

            platform="telegram"
        )

        db.add(lead)

        db.commit()



    response=await generate_response(
        text
    )



    message=models.Message(
        role="assistant",
        content=response
    )


    db.add(message)

    db.commit()

    db.close()



    await update.message.reply_text(
        response
    )



async def save_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):

    contact = update.message.contact

    db = SessionLocal()

    try:

        lead = db.query(
            models.Lead
        ).filter(
            models.Lead.telegram_chat_id == str(update.effective_chat.id)
        ).first()


        if lead:

            lead.phone = contact.phone_number
            lead.full_name = contact.first_name

            db.commit()


        else:

            lead = models.Lead(
                full_name=contact.first_name,
                phone=contact.phone_number,
                telegram_chat_id=str(update.effective_chat.id),
                platform="telegram"
            )

            db.add(lead)
            db.commit()


    except Exception as e:

        print(
            f"Contact save error: {e}"
        )

    finally:

        db.close()


    await update.message.reply_text(
        "✅ شماره تماس شما ثبت شد.\nحالا می‌توانید سوال خود را بپرسید."
    )


# --------------------------
# Run 24/7
# --------------------------


def run_bot():
    
    import asyncio


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


        # نگه داشتن بات روشن
        await asyncio.Event().wait()



    asyncio.run(start_bot())