import telebot
from database.connection import get_db_connection

def register_admin_handlers(bot):
    
    def is_admin(uid):
        conn = get_db_connection()
        res = conn.cursor().execute("SELECT role FROM users WHERE user_id = ?", (uid,)).fetchone()
        conn.close()
        return res and res['role'] in ['owner', 'admin']

    # 1. لوحة التحكم الرئيسية
    @bot.callback_query_handler(func=lambda call: call.data == "admin_panel")
    def admin_panel(call):
        if not is_admin(call.from_user.id): return
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton("➕/➖ النقاط", callback_data="admin_edit_points"),
            telebot.types.InlineKeyboardButton("⭐ ترقية VIP", callback_data="admin_give_vip"),
            telebot.types.InlineKeyboardButton("➕ مشروع", callback_data="admin_add_project"),
            telebot.types.InlineKeyboardButton("📢 إذاعة", callback_data="admin_broadcast"),
            telebot.types.InlineKeyboardButton("🛠 إدارة الفريق", callback_data="admin_manage_staff"),
            telebot.types.InlineKeyboardButton("✏️ مدير النصوص", callback_data="admin_edit_text"),
            telebot.types.InlineKeyboardButton("📊 إحصائيات", callback_data="admin_stats"),
            telebot.types.InlineKeyboardButton("🔙 عودة", callback_data="back_to_main")
        )
        bot.edit_message_text("👑 لوحة تحكم الأدمن:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # 2. مدير النصوص (تغيير الترحيب والأزرار)
    @bot.callback_query_handler(func=lambda call: call.data == "admin_edit_text")
    def choose_text_to_edit(call):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("ترحيب البوت", callback_data="edit_welcome_msg"))
        markup.add(telebot.types.InlineKeyboardButton("زر لايت موشن", callback_data="edit_btn_cat1"))
        markup.add(telebot.types.InlineKeyboardButton("زر أفتر إفكت", callback_data="edit_btn_cat2"))
        markup.add(telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel"))
        bot.edit_message_text("✏️ اختر النص الذي تريد تغييره:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("edit_"))
    def ask_new_text(call):
        key = call.data.replace("edit_", "")
        msg = bot.send_message(call.message.chat.id, f"📝 أرسل النص الجديد لـ ({key}):")
        bot.register_next_step_handler(msg, lambda m: save_custom_text(m, key))

    def save_custom_text(m, key):
        conn = get_db_connection()
        conn.cursor().execute("UPDATE settings SET value = ? WHERE key = ?", (m.text, key))
        conn.commit()
        conn.close()
        bot.send_message(m.chat.id, "✅ تم التحديث بنجاح!")

    # 3. إدارة الفريق
    @bot.callback_query_handler(func=lambda call: call.data == "admin_manage_staff")
    def manage_staff(call):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("➕ ترقية مشرف", callback_data="admin_add_admin"),
                   telebot.types.InlineKeyboardButton("🚫 طرد مستخدم", callback_data="admin_ban_user"),
                   telebot.types.InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel"))
        bot.edit_message_text("🛠 قسم إدارة الفريق:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # 4. دالات التنفيذ (ترقية، طرد، نقاط، إذاعة)
    @bot.callback_query_handler(func=lambda call: call.data == "admin_add_admin")
    def ask_admin_id(call):
        msg = bot.send_message(call.message.chat.id, "🆔 أرسل آيدي العضو لترقيته:")
        bot.register_next_step_handler(msg, lambda m: update_role(m, m.text, 'admin'))

    def update_role(m, uid, role):
        conn = get_db_connection()
        conn.cursor().execute("UPDATE users SET role = ? WHERE user_id = ?", (role, uid))
        conn.commit()
        conn.close()
        bot.send_message(m.chat.id, f"✅ تم تعيين `{uid}` كـ {role}.")

    @bot.callback_query_handler(func=lambda call: call.data == "admin_ban_user")
    def ask_ban_id(call):
        msg = bot.send_message(call.message.chat.id, "🆔 أرسل آيدي العضو للحظر:")
        bot.register_next_step_handler(msg, lambda m: ban_user(m, m.text))

    def ban_user(m, uid):
        conn = get_db_connection()
        conn.cursor().execute("UPDATE users SET is_banned = 1 WHERE user_id = ?", (uid,))
        conn.commit()
        conn.close()
        bot.send_message(m.chat.id, f"🚫 تم حظر `{uid}`.")

    @bot.callback_query_handler(func=lambda call: call.data == "admin_stats")
    def show_stats(call):
        conn = get_db_connection()
        count = conn.cursor().execute("SELECT COUNT(*) FROM users").fetchone()[0]
        conn.close()
        bot.answer_callback_query(call.id, f"👥 إجمالي المستخدمين: {count}", show_alert=True)

    # إضافة باقي الدالات (الإذاعة، المشاريع، النقاط، الـ VIP) كما في النسخ السابقة...
