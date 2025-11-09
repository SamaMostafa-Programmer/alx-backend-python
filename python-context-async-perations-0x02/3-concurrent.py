import asyncio
import aiosqlite

DB_NAME = 'async_app_database.db'

async def setup_database():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        await db.execute("INSERT OR REPLACE INTO users VALUES (1, 'Adam', 20)")
        await db.execute("INSERT OR REPLACE INTO users VALUES (2, 'Zahra', 45)")
        await db.execute("INSERT OR REPLACE INTO users VALUES (3, 'Youssef', 32)")
        await db.execute("INSERT OR REPLACE INTO users VALUES (4, 'Nora', 60)")
        await db.commit()
        print("Database setup complete.")


# 👇 لازم تكتبيها بالضبط كده (من غير مسافات أو arguments جوه الأقواس)
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        print("Starting to fetch ALL users...")
        await asyncio.sleep(0.5)
        async with db.execute("SELECT name, age FROM users") as cursor:
            results = await cursor.fetchall()
        print(f"Finished fetching ALL users ({len(results)} records).")
        return results


# 👇 نفس الفكرة هنا
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        age_limit = 40
        print(f"Starting to fetch users older than {age_limit}...")
        await asyncio.sleep(0.3)
        async with db.execute("SELECT name, age FROM users WHERE age > ?", (age_limit,)) as cursor:
            results = await cursor.fetchall()
        print(f"Finished fetching older users ({len(results)} records).")
        return results


async def fetch_concurrently():
    print("\n--- Starting Concurrent Fetching ---")
    
    # 👇 لاحظي استدعاء الدوال بدون تمرير db
    all_users_task, older_users_task = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("\n--- Results ---")
    print("All Users:")
    for name, age in all_users_task:
        print(f" - {name}, Age: {age}")
        
    print("\nUsers Older than 40:")
    for name, age in older_users_task:
        print(f" - {name}, Age: {age}")


if __name__ == "__main__":
    asyncio.run(setup_database())
    asyncio.run(fetch_concurrently())
