# AiCRM — AI Customer Acquisition & Booking Platform

## راه‌اندازی (Setup)

### پیش‌نیازها
- Node.js 18+
- Python 3.11+
- PostgreSQL

### فرانت‌اند

```bash
cd frontend
npm install
npm run dev
```

مرورگر رو باز کن و برو به: http://localhost:3000

### هفته ۱ — چی داریم؟
- [x] ساختار Next.js + TypeScript + Tailwind
- [x] دشبورد اصلی با آمار
- [x] سایدبار و ناوبری
- [x] نمودارها (Recharts)
- [x] لیست لیدهای اخیر
- [x] فید فعالیت AI
- [ ] صفحه Leads (هفته بعد)
- [ ] صفحه Conversations (هفته بعد)
- [ ] بک‌اند FastAPI (هفته ۲)

## ساختار پروژه

```
aicrm/
├── frontend/          # Next.js App
│   ├── src/
│   │   ├── app/
│   │   │   ├── dashboard/
│   │   │   │   ├── page.tsx       # صفحه اصلی
│   │   │   │   ├── leads/
│   │   │   │   ├── conversations/
│   │   │   │   ├── bookings/
│   │   │   │   └── analytics/
│   │   │   └── layout.tsx
│   │   └── components/
│   │       └── layout/
│   │           ├── Sidebar.tsx
│   │           └── Topbar.tsx
└── backend/           # FastAPI (هفته ۲)
```
