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

import os
import asyncio


load_dotenv()


# =========================
# Database Initialization
# =========================

Base.metadata.create_all(bind=engine)


# =========================
# FastAPI App
# =========================

app = FastAPI(
    title="Rozita AI CRM",
    description="AI-powered Customer Management Platform",
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
# Routers
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
        "name": "Rozita AI CRM",
        "status": "online"
    }



@app.get("/health")
def health():

    return {
        "status": "healthy"
    }



# =========================
# Telegram Control
# =========================

telegram_task = None


async def start_telegram():

    global telegram_task


    token = os.getenv(
        "TELEGRAM_BOT_TOKEN"
    )


    if not token:

        print(
            "⚠️ Telegram token missing"
        )

        return


    if telegram_task:

        print(
            "Telegram already running"
        )

        return



    from app.services.telegram_service import run_bot


    telegram_task = asyncio.create_task(
        asyncio.to_thread(run_bot)
    )


    print(
        "🤖 Telegram bot started"
    )



# =========================
# Startup / Shutdown
# =========================

@app.on_event("startup")
async def startup():

    await start_telegram()



@app.on_event("shutdown")
async def shutdown():

    global telegram_task


    if telegram_task:

        telegram_task.cancel()

        print(
            "Telegram bot stopped"
        )