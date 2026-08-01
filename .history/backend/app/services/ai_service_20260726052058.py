# نسخه بدون AI - با جواب‌های آماده
import json

RESPONSES = {
    "سلام": "سلام! 👋 به آژانس مارکتینگ رشدینو خوش اومدید. چطور می‌تونم کمکتون کنم؟",
    "قیمت": "قیمت‌های ما بسته به نوع خدمت متفاوته. پکیج پایه از ۶۰ میلیون تومان شروع میشه. می‌خواید یه جلسه رایگان داشته باشیم؟",
    "خدمات": "ما این خدمات رو داریم:\n✅ سئو\n✅ تبلیغات گوگل\n✅ مدیریت شبکه‌های اجتماعی\n✅ تولید محتوا\n✅ طراحی لندینگ\n✅ تحلیل داده\n\nکدوم براتون جالب‌تره؟",
    "جلسه": "عالیه! برای رزرو جلسه کشف نیاز (رایگان) لطفاً شماره تماستون رو بفرستید.",
    "default": "ممنون از پیامتون 🙏 برای پاسخ دقیق‌تر، لطفاً شماره تماستون رو بفرستید تا کارشناس ما باهاتون تماس بگیره."
}

def get_ai_response(messages: list, lead_info: dict = {}) -> str:
    if not messages:
        return RESPONSES["default"]
    
    last_msg = messages[-1].get("content", "").lower()
    
    for key in RESPONSES:
        if key != "default" and key in last_msg:
            return RESPONSES[key]
    
    return RESPONSES["default"]

def extract_lead_info(messages: list) -> dict:
    info = {}
    for msg in messages:
        content = msg.get("content", "")
        # شماره تلفن
        import re
        phone = re.search(r'09\d{9}', content)
        if phone:
            info["phone"] = phone.group()
    return info
def generate_response(message, lead_info=None):
    """
    Compatibility wrapper for telegram_service
    """

    if lead_info is None:
        lead_info = {}

    messages = [
        {
            "role": "user",
            "content": message
        }
    ]

    return get_ai_response(
        messages,
        lead_info
    )