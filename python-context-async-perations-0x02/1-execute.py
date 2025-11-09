import sqlite3

class ExecuteQuery:
    """
    Context manager that executes a specific SQL query with parameters,
    manages the connection, and returns the results.
    """
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.results = None

    def __enter__(self):
        # 1. فتح الاتصال بقاعدة البيانات
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()

        # تهيئة البيانات
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'Alice', 20)")
        cursor.execute("INSERT OR IGNORE INTO users VALUES (2, 'Bob', 35)")
        cursor.execute("INSERT OR IGNORE INTO users VALUES (3, 'Charlie', 50)")
        self.conn.commit()

        # 2. تنفيذ الاستعلام المحدد
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        
        # 3. إرجاع النتائج مباشرة
        return self.results

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # 4. إغلاق الاتصال وضمان حفظ التغييرات إذا كانت عملية كتابة
        if self.conn:
            # هنا نستخدم commit للتأكد من حفظ أي تغييرات محتملة
            # self.conn.commit() 
            self.conn.close()
            
        if exc_type:
            print(f"Error during query execution: {exc_value}")
            
        return False 

# استخدام Context Manager لتنفيذ استعلام مع وسائط
if __name__ == "__main__":
    target_query = "SELECT * FROM users WHERE age > ?"
    target_param = 25

    # عند الخروج من 'with' يتم إغلاق الاتصال تلقائياً
    with ExecuteQuery('app_database.db', target_query, (target_param,)) as older_users:
        print(f"Executing query: '{target_query}' with parameter: {target_param}")
        print("\nUsers older than 25:")
        for user in older_users:
            print(user)
