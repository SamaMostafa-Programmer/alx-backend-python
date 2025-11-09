import sqlite3

class DatabaseConnection:
    """
    Context manager to handle opening and closing database connections automatically.
    """
    def __init__(self, db_name='app_database.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # 1. فتح الاتصال بقاعدة البيانات
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        # تهيئة قاعدة البيانات وإضافة بعض البيانات
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        self.cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'Omar', 30)")
        self.cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'Layla', 22)")
        self.conn.commit()
        
        # 2. إرجاع كائن الاتصال ليتم استخدامه داخل جملة 'with'
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # 3. إغلاق الاتصال عند الخروج من نطاق 'with'
        if self.conn:
            self.conn.close()
        
        # يمكننا هنا التعامل مع الأخطاء (Rollback) إذا لزم الأمر
        if exc_type:
            print(f"An exception of type {exc_type} occurred: {exc_value}")
        
        # لا نقم بكتم الخطأ (نرجع None أو False)
        return False 

# استخدام Context Manager لتنفيذ الاستعلام
if __name__ == "__main__":
    results = []
    
    # يتم فتح الاتصال تلقائياً هنا
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        print("Database connection opened successfully.")
        
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        
    # يتم إغلاق الاتصال تلقائياً هنا
    print("Database connection closed.")
    
    print("\nQuery results:")
    for row in results:
        print(row)
