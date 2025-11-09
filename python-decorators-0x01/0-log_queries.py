import sqlite3
import functools

def log_queries(func):
    """
    Decorator that logs the SQL query before executing the function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # البحث عن حجة الاستعلام (query) في *args أو **kwargs
        # نفترض هنا أن الاستعلام هو أول حجة موضعية أو يتم تمريره كحجة query=...
        query = None
        
        # إذا كانت الدالة تستقبل الاستعلام كأول حجة موضعية
        if args:
            query = args[0]
        
        # إذا كانت الدالة تستقبل الاستعلام كحجة keyword باسم 'query'
        if not query and 'query' in kwargs:
            query = kwargs['query']

        if query:
            print(f"LOG: Executing SQL query -> {query}")
        else:
            print("LOG: Executing function without explicit query argument.")

        return func(*args, **kwargs)

    return wrapper

@log_queries
def fetch_all_users(query):
    # إنشاء قاعدة بيانات وهمية إذا لم تكن موجودة للتجربة
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    conn.commit()
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# #### fetch users while logging the query
# users = fetch_all_users(query="SELECT * FROM users")
# print(users)
