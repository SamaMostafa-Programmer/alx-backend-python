import sqlite3 
import functools

# نسخ معالج الاتصال من المهمة 1
def with_db_connection(func):
    """Opens connection, passes it to func, and closes it."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def transactional(func):
    """
    Decorator that wraps a function inside a database transaction, 
    committing changes on success or rolling back on exception.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # نتوقع أن تكون conn هي الحجة الأولى التي يوفرها with_db_connection
        try:
            result = func(conn, *args, **kwargs)
            conn.commit() # Commit on success
            print("Transaction committed successfully.")
            return result
        except Exception as e:
            conn.rollback() # Rollback on failure
            print(f"Transaction rolled back due to error: {e}")
            raise # إعادة رمي الخطأ ليبقى مرئياً

    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    # تهيئة قاعدة البيانات للتجربة
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", (1, 'Initial Name', 'initial@example.com'))
    
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    # يمكن إثارة خطأ هنا لاختبار Rollback
    # if user_id == 1:
    #     raise ValueError("Simulated error for rollback test")

# #### Update user's email with automatic transaction handling 
# update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
