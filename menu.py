from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu(user_role):
    """
    القائمة الرئيسية للبوت: تظهر الأزرار للجميع، 
    ولكن زر لوحة الأدمن يظهر فقط للمخولين.
    """
    markup = InlineKeyboardMarkup(row_width=2)
    
    # الصف الأول: المشاريع الأساسية
    markup.add(
        InlineKeyboardButton("🎬 لايت موشن", callback_data="cat_1"),
        InlineKeyboardButton("🎥 أفتر إفكت", callback_data="cat_2")
    )
    
    # الصف الثاني: الخدمات التفاعلية
    markup.add(
        InlineKeyboardButton("💎 نقاطي", callback_data="my_points"),
        InlineKeyboardButton("🏆 المتصدرون", callback_data="leaderboard")
    )
    
    # الصف الثالث: الـ VIP
    markup.add(InlineKeyboardButton("⭐ ترقية VIP", callback_data="vip_page"))
    
    # الصف الرابع: لوحة التحكم (تظهر فقط للأدمن أو المالك)
    if user_role in ['owner', 'admin']:
        markup.add(InlineKeyboardButton("👑 لوحة تحكم الأدمن", callback_data="admin_panel"))
        
    return markup

def get_back_menu():
    """
    زر للعودة للقائمة الرئيسية في أي قسم فرعي.
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="back_to_main"))
    return markup
