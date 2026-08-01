"use client";
import { Phone, Plus, Clock } from "lucide-react";
import { useState, useEffect } from "react";

export default function CallsPage() {
  const [conversations, setConversations] = useState<any[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [selectedConv, setSelectedConv] = useState<number | null>(null);
  const [duration, setDuration] = useState("");
  const [notes, setNotes] = useState("");

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/conversations/");
      if (res.ok) {
        const data = await res.json();
        setConversations(data);
      }
    } catch (err) {
      console.error("Error:", err);
    }
  };

  const handleLogCall = async () => {
    if (!selectedConv || !duration) {
      alert("لطفا گفتگو و مدت تماس رو انتخاب کن");
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/api/calls/log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: selectedConv,
          duration_minutes: parseInt(duration),
          notes: notes
        })
      });

      if (res.ok) {
        alert("✅ تماس ثبت شد!");
        setDuration("");
        setNotes("");
        setShowForm(false);
        fetchConversations();
      }
    } catch (err) {
      alert("❌ خطا!");
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-white flex items-center gap-2">
          <Phone className="w-5 h-5 text-accent" />
          Call Tracking
        </h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-accent hover:bg-accent-hover text-white px-4 py-2 rounded-xl flex items-center gap-2 text-sm"
        >
          <Plus className="w-4 h-4" />
          تماس جدید
        </button>
      </div>

      {showForm && (
        <div className="glass-card p-6">
          <h2 className="text-white font-medium mb-4">ثبت تماس تلفنی</h2>
          
          <div className="space-y-4">
            <div>
              <label className="text-slate-300 text-sm mb-2 block">مشتری</label>
              <select
                value={selectedConv || ""}
                onChange={(e) => setSelectedConv(parseInt(e.target.value))}
                className="input-dark"
              >
                <option value="">انتخاب کن...</option>
                {conversations.map((conv) => (
                  <option key={conv.id} value={conv.id}>
                    {conv.lead?.full_name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-slate-300 text-sm mb-2 block">مدت (دقیقه)</label>
              <input
                type="number"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                placeholder="15"
                className="input-dark"
              />
            </div>

            <div>
              <label className="text-slate-300 text-sm mb-2 block">یادداشت</label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="موضوع تماس..."
                className="input-dark"
                rows={3}
              />
            </div>

            <button
              onClick={handleLogCall}
              className="bg-accent hover:bg-accent-hover text-white px-4 py-2 rounded-xl w-full"
            >
              ✓ ثبت تماس
            </button>
          </div>
        </div>
      )}

      <div className="glass-card">
        <div className="flex items-center justify-between p-5 border-b border-pink-500/10">
          <h2 className="text-sm font-medium text-white">مشتریان</h2>
        </div>
        
        <div className="divide-y divide-pink-500/[0.06]">
          {conversations.length === 0 ? (
            <div className="p-5 text-center text-slate-600 text-sm">مشتریای وجود ندارد</div>
          ) : (
            conversations.map((conv) => (
              <div key={conv.id} className="p-5 hover:bg-white/[0.02]">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-white font-medium">{conv.lead?.full_name}</p>
                    <p className="text-slate-600 text-xs mt-1 flex items-center gap-1">
                      <Clock className="w-3 h-3" />
                      {conv.messages.length} پیام
                    </p>
                  </div>
                  <span className="text-yellow-400 text-xs px-2 py-1 bg-yellow-400/10 rounded">
                    {conv.platform}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
