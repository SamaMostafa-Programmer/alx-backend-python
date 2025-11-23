import time
import sqlite3 
import functools

# معالج الاتصال
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

def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries the wrapped function a certain number of times 
    if it raises an exception, waiting a specified delay between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {i + 1} failed. Retrying in {delay} seconds...")
                    time.sleep(delay)
            
            # إذا فشلت كل المحاولات، نثير آخر خطأ حدث
            print(f"All {retries} attempts failed.")
            raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    # إنشاء قاعدة بيانات للتجربة
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    
    # محاكاة خطأ متقطع (Transient Error):
    # يمكن وضع شرط لإثارة خطأ في أول محاولة أو محاولتين
    # global attempt_count
    # attempt_count += 1
    # if attempt_count <= 2:
    #     raise sqlite3.OperationalError("Database is locked/Busy - Simulated failure")

    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# #### attempt to fetch users with automatic retry on failure
# # يجب تعريف متغير attempt_count = 0 عالمياً قبل الاختبار إذا كنت ستستخدم محاكاة الخطأ المتقطع
# users = fetch_users_with_retry()
# print(users)
