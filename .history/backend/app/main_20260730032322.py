from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import (
    leads,
    conversations,
    bookings,
    analytics,
    exports,
    calls,
    excel_export
)

from dotenv import load_dotenv

import threading
import os


load_dotenv()


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Rozita AI CRM",
    description="AI-powered Customer Management",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# API Routers
# =========================

app.include_router(
    leads.router,
    prefix="/api"
)


app.include_router(
    conversations.router,
    prefix="/api"
)


app.include_router(
    bookings.router,
    prefix="/api"
)


app.include_router(
    analytics.router,
    prefix="/api"
)


app.include_router(
    exports.router,
    prefix="/api"
)


app.include_router(
    calls.router,
    prefix="/api"
)


app.include_router(
    excel_export.router,
    prefix="/api"
)



# =========================
# Health
# =========================

@app.get("/")
def root():

    return {
        "message": "Rozita AI CRM",
        "version": "1.0.0"
    }



@app.get("/health")
def health():

    return {
        "status": "healthy"
    }



# =========================
# Telegram Startup
# =========================

@app.on_event("startup")
async def startup():

    token = os.getenv(
        "TELEGRAM_BOT_TOKEN"
    )


    if token:

        from app.services.telegram_service import run_bot


        bot_thread = threading.Thread(
            target=run_bot,
            daemon=True
        )


        bot_thread.start()


        print("✅ Telegram bot started")


    else:

        print(
            "⚠️ Telegram token missing"
        )