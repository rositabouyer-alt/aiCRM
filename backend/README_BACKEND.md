# راه‌اندازی بک‌اند

## ۱. نصب پکیج‌ها
```bash
cd aicrm/backend
pip install -r requirements.txt
```

## ۲. نصب PostgreSQL
از سایت postgresql.org نصب کن، بعد:
```sql
CREATE DATABASE aicrm;
```

## ۳. تنظیم .env
فایل `.env` رو باز کن و پر کن:
- DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/aicrm
- TELEGRAM_BOT_TOKEN=توکن تلگرام بات
- GROQ_API_KEY=کلید Groq (رایگان از groq.com)

## ۴. اجرا
```bash
python run.py
```

بک‌اند روی http://localhost:8000 بالا میاد
مستندات API: http://localhost:8000/docs

## ۵. گرفتن توکن تلگرام
۱. به @BotFather توی تلگرام برو
۲. بنویس /newbot
۳. اسم بات رو بده
۴. توکن رو کپی کن توی .env

## ۶. گرفتن Groq API (رایگان)
۱. برو به console.groq.com
۲. ثبت‌نام کن
۳. API Key بگیر
۴. توی .env بذار
