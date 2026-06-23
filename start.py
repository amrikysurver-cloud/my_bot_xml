import telebot
from database.connection import get_db_connection
from keyboards.inline import get_main_menu

def register_start_handlers(bot):
    
    @bot.message_handler(commands=['start'])
    def start_command(message):
        user_id = message.from_user.id
        username = message.from_user.username
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. تسجيل المستخدم
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username, role) VALUES (?, ?, ?)", 
                       (user_id, username, 'user'))
        conn.commit()
        
        # 2. التحقق من الحظر والرتبة
        cursor.execute("SELECT role, is_banned FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()
        
        # 3. جلب نص الترحيب من قاعدة البيانات
        cursor.execute("SELECT value FROM settings WHERE key = 'welcome_msg'")
        welcome_text = cursor.fetchone()['value']
        conn.close()
        
        # 4. نظام الحماية
        if user_data and user_data['is_banned'] == 1:
            bot.send_message(message.chat.id, "❌ عذراً، أنت محظور من استخدام البوت.")
            return
            
        user_role = user_data['role'] if user_data else 'user'
        
        # 5. إرسال القائمة
        bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(user_role))

    # دالة العودة للقائمة الرئيسية (callback)
    @bot.callback_query_handler(func=lambda call: call.data == "back_to_main")
    def back_to_main(call):
        conn = get_db_connection()
        user = conn.cursor().execute("SELECT role FROM users WHERE user_id = ?", (call.from_user.id,)).fetchone()
        user_role = user['role'] if user else 'user'
        conn.close()
        
        bot.edit_message_text(
            "🔙 القائمة الرئيسية:", 
            call.message.chat.id, 
            call.message.message_id, 
            reply_markup=get_main_menu(user_role)
        )
