import sqlite3
import functools
from datetime import datetime # تمت الإضافة هنا بناءً على الملاحظة

#### decorator to log SQL queries

def log_queries(func):
    """
    Decorator that logs the SQL query before executing the function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # محاولة استخلاص الاستعلام
        query = args[0] if args and isinstance(args[0], str) else kwargs.get('query')

        if query:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] LOG: Executing SQL query -> {query}")
        
        return func(*args, **kwargs)

    return wrapper

@log_queries
def fetch_all_users(query):
    # إعداد قاعدة بيانات للتجربة
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    conn.commit()
    
    # تنفيذ الاستعلام
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print("Fetched users count:", len(users))
