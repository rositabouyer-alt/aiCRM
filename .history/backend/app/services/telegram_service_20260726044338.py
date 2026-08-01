import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
from app.database import SessionLocal
from app import models

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("8884657674:AAHFy6GW4JRO7gyCsvMQH5F4IQVCtZtGwMU")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db = SessionLocal()
    
    # Check/Create Lead
    lead = db.query(models.Lead).filter(models.Lead.phone == str(user.id)).first()
    if not lead:
        lead = models.Lead(
            full_name=user.first_name or "Unknown",
            phone=str(user.id),
            platform="telegram",
            telegram_chat_id=str(update.effective_chat.id)
        )
        db.add(lead)
        db.flush()
    
    # Check/Create Conversation
    conv = db.query(models.Conversation).filter(
        models.Conversation.platform_chat_id == str(update.effective_chat.id)
    ).first()
    if not conv:
        conv = models.Conversation(
            lead_id=lead.id,
            platform="telegram",
            platform_chat_id=str(update.effective_chat.id)
        )
        db.add(conv)
    
    db.commit()
    db.close()
    
    welcome = f"سلام {user.first_name}! 👋\n\nبه Lumora خوش اومدید.\n\nمی‌تونم کمکتون کنم با:\n- پاسخ به سوال‌ها\n- رزرو جلسات\n- اطلاعات محصولات"
    await update.message.reply_text(welcome)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        text = update.message.text
        
        db = SessionLocal()
        
        # Get/Create Lead
        lead = db.query(models.Lead).filter(models.Lead.phone == str(user.id)).first()
        if not lead:
            lead = models.Lead(
                full_name=user.first_name or "Unknown",
                phone=str(user.id),
                platform="telegram",
                telegram_chat_id=str(update.effective_chat.id)
            )
            db.add(lead)
            db.flush()
        
        # Get/Create Conversation
        conv = db.query(models.Conversation).filter(
            models.Conversation.platform_chat_id == str(update.effective_chat.id)
        ).first()
        if not conv:
            conv = models.Conversation(
                lead_id=lead.id,
                platform="telegram",
                platform_chat_id=str(update.effective_chat.id)
            )
            db.add(conv)
            db.flush()
        
        # Save User Message
        user_msg = models.Message(
            conversation_id=conv.id,
            role="user",
            content=text
        )
        db.add(user_msg)
        db.commit()
        
        # AI Response
        response = "سپاس برای پیامت! 😊\n\nتیم ما به زودی جواب می‌دهند."
        
        # Save Bot Response
        bot_msg = models.Message(
            conversation_id=conv.id,
            role="assistant",
            content=response
        )
        db.add(bot_msg)
        db.commit()
        db.close()
        
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Error: {e}")

async def main():
    if not TELEGRAM_BOT_TOKEN:
        logger.warning("No token")
        return
    
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("✅ Telegram Bot Started!")
    await app.run_polling()

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except Exception as e:
        logger.error(f"Bot Error: {e}")
