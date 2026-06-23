from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.connection import get_db_connection

def get_main_menu(user_role):
    """
    القائمة الرئيسية: تقرأ نصوص الأزرار من قاعدة البيانات ديناميكياً.
    """
    conn = get_db_connection()
    # جلب جميع نصوص الأزرار من قاعدة البيانات
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settings WHERE key LIKE 'btn_%'")
    texts = {row['key']: row['value'] for row in cursor.fetchall()}
    conn.close()
    
    # تحديد نصوص الأزرار بناءً على ما في قاعدة البيانات أو القيم الافتراضية
    btn_cat1_text = texts.get('btn_cat1', '🎬 لايت موشن')
    btn_cat2_text = texts.get('btn_cat2', '🎥 أفتر إفكت')
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    # الصف الأول: المشاريع
    markup.add(
        InlineKeyboardButton(btn_cat1_text, callback_data="cat_1"),
        InlineKeyboardButton(btn_cat2_text, callback_data="cat_2")
    )
    
    # الصف الثاني: الخدمات التفاعلية
    markup.add(
        InlineKeyboardButton("💎 نقاطي", callback_data="my_points"),
        InlineKeyboardButton("🏆 المتصدرون", callback_data="leaderboard")
    )
    
    # الصف الثالث: ترقية VIP
    markup.add(InlineKeyboardButton("⭐ ترقية VIP", callback_data="vip_page"))
    
    # الصف الرابع: لوحة التحكم (للأدمن فقط)
    if user_role in ['owner', 'admin']:
        markup.add(InlineKeyboardButton("👑 لوحة تحكم الأدمن", callback_data="admin_panel"))
        
    return markup

def get_back_menu():
    """
    زر العودة الموحد.
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main"))
    return markup
