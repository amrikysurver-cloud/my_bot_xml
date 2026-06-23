import sqlite3

def get_db_connection():
    """
    يفتح اتصالاً بقاعدة البيانات ويعيد كائناً للتعامل مع البيانات كصفوف (Rows).
    """
    conn = sqlite3.connect("bot_database.db")
    conn.row_factory = sqlite3.Row  # لتتمكن من الوصول للبيانات عن طريق أسماء الأعمدة
    return conn

def init_db():
    """
    تقوم بإنشاء الجداول في حال عدم وجودها، وتجهيز البيانات الافتراضية.
    """
    conn = get_db_connection()
    c = conn.cursor()
    
    # 1. جدول المستخدمين (مع دعم الرتب، النقاط، الـ VIP، والحظر)
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            role TEXT DEFAULT 'user',
            points INTEGER DEFAULT 0,
            is_vip INTEGER DEFAULT 0,
            is_banned INTEGER DEFAULT 0
        )
    """)
    
    # 2. جدول المشاريع (لتخزين المحتوى)
    c.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category_id INTEGER,
            download_links TEXT
        )
    """)
    
    # 3. جدول الإعدادات (للتحكم في النصوص ديناميكياً)
    c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)
    
    # إدخال نص الترحيب الافتراضي إذا لم يكن موجوداً
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('welcome_msg', 'أهلاً بك في البوت الإمبراطوري!')")
    
    conn.commit()
    conn.close()
