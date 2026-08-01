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


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Rozita AI CRM",
    description="AI-powered Customer Management",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# =====================
# Routers
# =====================

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



@app.get("/")
def root():

    return {
        "message": "Rozita AI CRM",
        "version": "1.0.0"
    }



@app.get("/health")
def health():

    return {
        "status":"healthy"
    }



telegram_task = None



@app.on_event("startup")
async def startup():


    global telegram_task


    token = os.getenv(
        "TELEGRAM_BOT_TOKEN"
    )


    if not token:

        print(
            "⚠️ Telegram token missing"
        )

        return



    # جلوگیری از اجرای دوباره در reload

    if telegram_task:

        return



    from app.services.telegram_service import start_bot



    telegram_task = asyncio.create_task(
        start_bot()
    )


    print(
        "✅ Telegram bot started"
    )



@app.on_event("shutdown")
async def shutdown():

    global telegram_task


    if telegram_task:

        telegram_task.cancel()

        telegram_task = None