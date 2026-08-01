from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import leads, conversations, bookings, analytics, exports, calls, excel_export
import threading
from dotenv import load_dotenv
import os

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rozita AI CRM",
    description="AI-powered Customer Management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leads.router, prefix="/api")
app.include_router(conversations.router, prefix="/api")
app.include_router(bookings.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(exports.router, prefix="/api")
app.include_router(calls.router, prefix="/api")
app.include_router(excel_export.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Rozita AI CRM", "version": "1.0.0"}

@app.on_event("startup")
async def startup():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if token:
        from app.services.telegram_service import run_bot
        t = threading.Thread(target=run_bot, daemon=True)
        t.start()
        print("✅ Telegram bot started")
