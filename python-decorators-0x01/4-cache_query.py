import time
import sqlite3 
import functools

query_cache = {}

# معالج الاتصال (ضروري لتشغيل الكود)
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

def cache_query(func):
    """
    Decorator that caches query results based on the SQL query string 
    (assumes the query is the last positional or keyword argument).
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # استخراج الاستعلام لتوليد المفتاح (key) للتخزين المؤقت
        query = None
        
        # البحث في الحجج الموضعية (بعد conn)
        if args:
            # نفترض أن الاستعلام هو آخر حجة موضعية بعد conn
            query = args[-1] 
        # البحث في حجج الكلمات المفتاحية
        elif 'query' in kwargs:
            query = kwargs['query']
        
        # إذا وجد الاستعلام وكان في الذاكرة المؤقتة، إرجاع النتيجة المحفوظة
        if query in query_cache:
            print(f"CACHE HIT: Returning cached result for query: {query}")
            return query_cache[query]

        # إذا لم يكن في الذاكرة المؤقتة، تنفيذ الدالة الأصلية
        print(f"CACHE MISS: Executing query: {query}")
        result = func(conn, *args, **kwargs)
        
        # حفظ النتيجة في الذاكرة المؤقتة قبل الإرجاع
        if query:
            query_cache[query] = result
            
        return result

    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    # تهيئة قاعدة البيانات للتجربة
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    
    # طباعة رسالة لتوضيح متى يتم فعلاً الوصول إلى قاعدة البيانات
    print("--- ACCESSING DATABASE ---") 
    cursor.execute(query)
    return cursor.fetchall()

# #### First call will cache the result
# users = fetch_users_with_cache(query="SELECT * FROM users")
# print("First call result:", users)

# #### Second call will use the cached result
# users_again = fetch_users_with_cache(query="SELECT * FROM users")
# print("Second call result:", users_again)

# print("Cache content:", query_cache)
