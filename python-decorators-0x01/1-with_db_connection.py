import sqlite3 
import functools

def with_db_connection(func):
    """
    Decorator that opens a database connection, passes it to the function 
    as the first argument, and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # تمرير كائن الاتصال (conn) كأول حجة (positional argument)
            # ثم تمرير باقي الحجج
            result = func(conn, *args, **kwargs) 
            return result
        finally:
            # ضمان إغلاق الاتصال حتى لو حدث خطأ
            conn.close()
    
    return wrapper 

@with_db_connection 
def get_user_by_id(conn, user_id): 
    # تهيئة قاعدة البيانات للتجربة
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", (1, 'Alice', 'alice@example.com'))
    conn.commit()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 

# #### Fetch user by ID with automatic connection handling 
# user = get_user_by_id(user_id=1)
# print(user)
