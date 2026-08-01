# 🚀 Rozita AI CRM - Complete Project

**پروژه کامل و آماده برای استفاده فوری**

---

## 📦 چی در بسته است؟

```
✅ فرانت‌اند (Next.js + Tailwind + Pink Neon)
   - Dashboard (آمار شامل)
   - Leads Management (جدول + فیلتر)
   - Conversations (چت رئال‌تایم)
   - Bookings (رزرو جلسات)
   - Settings

✅ بک‌اند (FastAPI + PostgreSQL)
   - Telegram Integration (توکن واقعی)
   - Instagram Integration (کد آماده)
   - WhatsApp Integration (کد آماده)
   - AI Chatbot (پاسخ‌های هوشمند)
   - Lead Management API
   - Booking System API
   - Analytics API

✅ دیتابیس
   - Leads, Conversations, Messages, Bookings
   - Platform Integration Support
```

---

## ⚡ شروع سریع (30 دقیقه)

### الف) فرانت‌اند

```bash
cd frontend
npm install
npm run dev
```

ورود: http://localhost:3000

### ب) بک‌اند

```bash
# ۱. PostgreSQL نصب کن و دیتابیس بساز
createdb -U postgres roziai

# ۲. Dependencies نصب کن
cd backend
pip install fastapi uvicorn sqlalchemy alembic python-dotenv pydantic pydantic-settings python-telegram-bot openai python-jose passlib bcrypt python-multipart httpx

# ۳. اجرا
python run.py
```

ورود API: http://localhost:8000/docs

---

## 🔧 تنظیمات

### `.env` - تنظیمات پایه

```dotenv
# Database
DATABASE_URL=postgresql://postgres:rozita56@localhost:5432/roziai

# Security
SECRET_KEY=RozAI_2025_SuperSecret_Key_123456789

# Telegram Bot (ACTIVE)
TELEGRAM_BOT_TOKEN=8884657674:AAHFy6GW4JRO7gyCsvMQH5F4IQVCtZtGwMU

# Instagram (Ready - just add token when available)
INSTAGRAM_ACCESS_TOKEN=
INSTAGRAM_BUSINESS_ACCOUNT_ID=

# App
APP_NAME=Rozita AI CRM
FRONTEND_URL=http://localhost:3000
```

### Telegram را اول کنید ✅

توکن داری! فوری مشتریان می‌تونن تلگرام بفرستن.

### Instagram (آماده برای بعداً)

**وقتی Meta تأیید کرد:**

۱. برو به https://business.facebook.com/
۲. Apps → Create App → Instagram
۳. Get Access Token
۴. `.env` رو آپدیت کن
۵. Restart Backend

همین!

---

## 🔌 چگونه تلگرام کار می‌کنه الان

```
User (Telegram)
    ↓
Bot (Token: 8884657674:AAHFy...)
    ↓
FastAPI Backend
    ↓
PostgreSQL (Lead + Conversation + Messages)
    ↓
Rozita CRM Dashboard (مشاهده / جواب دادن)
```

**فوری پیام می‌رسه!** 🔥

---

## 📊 چی می‌کنه هر بخش

### Dashboard
- آمار شامل (Leads, Conversations, Bookings, Conversion Rate)
- نمودارهای واقعی
- فید فعالیت AI

### Leads
- لیست تمام مشتریان
- فیلتر بر اساس وضعیت/پلتفرم
- جستجو
- Export

### Conversations
- تمام پیام‌ها از تلگرام (و بعداً Instagram)
- رئال‌تایم updatesّ
- جواب مستقیم
- Toggle AI On/Off

### Bookings
- رزرو خودکار از چت
- تایید/لغو
- تقویم

---

## 🤖 AI Chatbot

**فعلاً:** Responses آماده مثل:
- سلام → جواب خوشامدگویی
- قیمت → جواب قیمت‌ها
- جلسه → درخواست شماره تماس

**بعداً:** Groq API سازش (وقتی VPN حل شد)

---

## 📱 کانال‌ها

### ✅ Telegram - ACTIVE NOW
- توکن واقعی
- Webhook یا Polling
- Message Sync خودکار

### 🔄 Instagram - Ready (Code)
```python
# فایل: app/services/instagram_service.py
# وقتی token بگیری، فعال می‌شه
```

### 🔄 WhatsApp - Ready (Code)
```python
# فایل: app/services/whatsapp_service.py
# وقتی Meta Verified شی
```

### 🔄 Website Chat - Ready (Code)
```javascript
// Widget برای وب‌سایت آماده‌ست
```

---

## 🚨 مشکلات و حل‌ها

### Database Connection Error
```bash
# ✅ PostgreSQL باید روی پورت ۵۴۳۲ اجرا شود
# ✅ User: postgres, Password: rozita56
# ✅ Database: roziai

# Test:
psql -U postgres -d roziai
```

### Telegram Token Not Working
```bash
# ✅ توکن دقیق است و واقعی است
# ✅ اگر کار نکرد، بات جدید بساز:
# @BotFather → /newbot
```

### Instagram/WhatsApp Not Connected
```
# عادی است! کد نوشته شده و منتظر API Keys
# Step-by-step guide در README بالا
```

---

## 📞 Telegram Bot استفاده

۱. **Search: @RozitaAICRMBot** (یا توکن خودت)
۲. **/start** بفرست
۳. شروع کن سؤال پرسیدن!

**نمونه:**
```
User: سلام
Bot: سلام! به آژانس مارکتینگ رشدینو خوش اومدید. چطور می‌تونم کمکتون کنم؟

User: قیمت سئو؟
Bot: قیمت‌های ما بسته به نوع خدمت متفاوته...
```

---

## 🔐 Security Notes

```
⚠️ SECRET_KEY: تغییر بده production میں
⚠️ CORS: localhost فقط - production میں تغییر بده
⚠️ Database Password: تغییر بده!
```

---

## 📊 Database Schema

```
Leads
├── id, full_name, phone, age, budget
├── platform (telegram, instagram, whatsapp, website)
├── status (new, active, qualified, booked, closed)
└── ai_summary

Conversations
├── id, lead_id, platform, platform_chat_id
├── is_ai_active
└── messages

Messages
├── id, conversation_id, role (user/assistant/admin)
└── content, created_at

Bookings
├── id, lead_id, scheduled_at, duration_minutes
├── status (pending, confirmed, cancelled)
└── notes
```

---

## 🚀 Deploy

### Vercel (Frontend)
```bash
cd frontend
vercel deploy
```

### Railway/Heroku (Backend)
```bash
cd backend
# heroku create
# heroku addons:create heroku-postgresql:hobby-dev
# git push heroku main
```

---

## 🎯 بعدی چی؟

**فاز بعدی (ماه دوم):**
- [ ] WhatsApp Integration
- [ ] Instagram Full Integration
- [ ] Advanced Lead Scoring
- [ ] Calendar Integration (Google Calendar)
- [ ] Email Integration

---

## 💬 Support

مسائل؟ سوالات؟

۱. **Backend مشکل:** logs رو چک کن
   ```bash
   tail -f logs/app.log
   ```

۲. **Frontend مشکل:** Browser console
   ```javascript
   // F12 → Console
   ```

۳. **Database مشکل:**
   ```bash
   psql -U postgres -d roziai
   \dt  # See all tables
   ```

---

**ساخت شده با ❤️ برای رشدینو**

*آماده برای تحویل تا 6 مرداد ✅*
