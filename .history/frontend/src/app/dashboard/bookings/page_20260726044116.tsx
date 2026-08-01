"use client";
import { CalendarCheck, Plus, Clock, User, MapPin } from "lucide-react";

const bookings = [
  { id: 1, name: "Sara Ahmadi", date: "شنبه ۱۰ صبح", service: "مشاوره سئو", duration: "30 دقیقه", status: "تایید شده" },
  { id: 2, name: "Ali Rezaei", date: "یکشنبه ۲ بعدازظهر", service: "تبلیغات گوگل", duration: "۱ ساعت", status: "در انتظار" },
  { id: 3, name: "Mina Hosseini", date: "دوشنبه ۹ صبح", service: "طراحی لندینگ", duration: "۱.۵ ساعت", status: "تایید شده" },
];

export default function BookingsPage() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-white flex items-center gap-2">
          <CalendarCheck className="w-5 h-5 text-accent" />
          Bookings
        </h1>
        <button className="btn-primary">
          <Plus className="w-4 h-4" /> New Booking
        </button>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {bookings.map((booking) => (
          <div key={booking.id} className="glass-card p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-white font-semibold">{booking.name}</h3>
                <p className="text-slate-600 text-sm">{booking.service}</p>
              </div>
              <span className={`text-xs px-3 py-1 rounded-full ${
                booking.status === "تایید شده" 
                  ? "bg-emerald-500/15 text-emerald-400" 
                  : "bg-yellow-500/15 text-yellow-400"
              }`}>
                {booking.status}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-4">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-accent" />
                <div>
                  <p className="text-slate-600 text-xs">وقت</p>
                  <p className="text-white text-sm font-medium">{booking.date}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <MapPin className="w-4 h-4 text-accent" />
                <div>
                  <p className="text-slate-600 text-xs">مدت زمان</p>
                  <p className="text-white text-sm font-medium">{booking.duration}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <User className="w-4 h-4 text-accent" />
                <div>
                  <p className="text-slate-600 text-xs">مشتری</p>
                  <p className="text-white text-sm font-medium">{booking.name}</p>
                </div>
              </div>
            </div>

            <div className="flex gap-2 mt-4 pt-4 border-t border-pink-500/[0.06]">
              <button className="btn-primary text-xs">Confirm</button>
              <button className="btn-ghost text-xs">Reschedule</button>
              <button className="btn-ghost text-xs">Cancel</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
