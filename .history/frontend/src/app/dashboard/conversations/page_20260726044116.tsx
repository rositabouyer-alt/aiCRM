"use client";
import { MessageSquare, Send, Phone, User } from "lucide-react";
import { useState, useEffect } from "react";

interface Message {
  id: number;
  role: string;
  content: string;
  created_at: string;
}

interface Lead {
  id: number;
  full_name: string;
  phone: string;
  platform: string;
  status: string;
}

interface Conversation {
  id: number;
  platform: string;
  is_ai_active: boolean;
  lead: Lead | null;
  messages: Message[];
  created_at: string;
}

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchConversations();
    const interval = setInterval(fetchConversations, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchConversations = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/conversations/");
      if (!res.ok) throw new Error("Failed to fetch");
      const data = await res.json();
      setConversations(data);
      if (data.length > 0 && !selected) setSelected(data[0].id);
      setLoading(false);
    } catch (err) {
      console.error("Error:", err);
      setLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!message.trim() || !selected) return;
    try {
      const res = await fetch(`http://localhost:8000/api/conversations/${selected}/send`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ conversation_id: selected, content: message })
      });
      if (res.ok) {
        setMessage("");
        fetchConversations();
      }
    } catch (err) {
      console.error("Error:", err);
    }
  };

  const active = conversations.find(c => c.id === selected);

  if (loading) {
    return (
      <div className="space-y-6">
        <h1 className="text-xl font-semibold text-white flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-accent" />
          Conversations
        </h1>
        <div className="flex items-center justify-center h-96">
          <p className="text-slate-400">درحال بارگیری...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <h1 className="text-xl font-semibold text-white flex items-center gap-2">
        <MessageSquare className="w-5 h-5 text-accent" />
        Conversations
      </h1>

      <div className="grid grid-cols-3 gap-4 h-[600px]">
        <div className="glass-card overflow-y-auto">
          {conversations.length === 0 ? (
            <div className="p-5 text-center text-slate-600 text-sm">هنوز مکالمه‌ای وجود ندارد</div>
          ) : (
            conversations.map((conv) => (
              <div
                key={conv.id}
                onClick={() => setSelected(conv.id)}
                className={`p-4 border-b border-pink-500/[0.06] cursor-pointer transition-all ${
                  selected === conv.id ? "bg-accent/10 border-accent/20" : "hover:bg-white/[0.02]"
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-accent to-violet-500 flex items-center justify-center text-white font-bold text-sm shrink-0">
                    {conv.lead?.full_name?.[0] || "?"}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-white text-sm font-medium">{conv.lead?.full_name || "Unknown"}</p>
                    <p className="text-slate-600 text-xs">{conv.platform} • {conv.messages.length} پیام</p>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="col-span-2 glass-card flex flex-col">
          {active ? (
            <>
              <div className="flex items-center justify-between p-4 border-b border-pink-500/[0.06]">
                <div className="flex items-center gap-3">
                  <User className="w-4 h-4 text-accent" />
                  <div>
                    <p className="text-white font-medium text-sm">{active.lead?.full_name}</p>
                    <p className="text-slate-600 text-xs">{active.platform} • {active.lead?.phone}</p>
                  </div>
                </div>
                <button className="btn-ghost">
                  <Phone className="w-4 h-4" />
                </button>
              </div>

              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {active.messages.length === 0 ? (
                  <div className="flex items-center justify-center h-full text-slate-600">
                    هنوز پیامی وجود ندارد
                  </div>
                ) : (
                  active.messages.map((msg) => (
                    <div key={msg.id} className={`flex ${msg.role === "user" ? "justify-start" : "justify-end"}`}>
                      <div className={`rounded-lg px-4 py-2 max-w-xs break-words ${
                        msg.role === "user" ? "bg-white/[0.08]" : "bg-accent/20 border border-accent/30"
                      }`}>
                        <p className={`text-sm ${msg.role === "user" ? "text-slate-300" : "text-white"}`}>
                          {msg.content}
                        </p>
                        <p className="text-slate-600 text-xs mt-1">
                          {new Date(msg.created_at).toLocaleTimeString("fa-IR")}
                        </p>
                      </div>
                    </div>
                  ))
                )}
              </div>

              <div className="border-t border-pink-500/[0.06] p-4 flex gap-2">
                <input
                  type="text"
                  placeholder="جواب بده..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                  className="input-dark flex-1"
                />
                <button onClick={handleSendMessage} className="bg-accent hover:bg-accent-hover text-white font-medium px-4 py-2 rounded-xl transition-all text-sm">
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </>
          ) : (
            <div className="flex items-center justify-center h-full">
              <p className="text-slate-400">مکالمه‌ای انتخاب کن</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
