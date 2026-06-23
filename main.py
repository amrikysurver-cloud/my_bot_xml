import os
import telebot
import logging
from database.connection import init_db
from handlers.start import register_start_handlers
from handlers.admin import register_admin_handlers

# إعداد السجلات (Logs) لمتابعة حالة البوت على السيرفر
logging.basicConfig(level=logging.INFO)

# التوكن يتم جلبه من متغيرات البيئة (Environment Variables) في السيرفر
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

def run_bot():
    try:
        print("⚙️ تهيئة قاعدة البيانات...")
        init_db()
        
        print("🔗 تسجيل الأوامر...")
        register_start_handlers(bot)
        register_admin_handlers(bot)
        
        print("🚀 البوت يعمل الآن بكامل طاقته (نظام الاستضافة الدائمة)!")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
        
    except Exception as e:
        logging.error(f"حدث خطأ في التشغيل: {e}")

if __name__ == "__main__":
    run_bot()
