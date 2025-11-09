import asyncio
import aiosqlite

DB_NAME = 'async_app_database.db'

async def setup_database():
    """
    Creates the database file and populates it with initial data asynchronously.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        
        # Insert sample data
        await db.execute("INSERT OR REPLACE INTO users VALUES (1, 'Adam', 20)")
        await db.execute("INSERT OR REPLACE INTO users VALUES (2, 'Zahra', 45)")
        await db.execute("INSERT OR REPLACE INTO users VALUES (3, 'Youssef', 32)")
        await db.execute("INSERT OR REPLACE INTO users VALUES (4, 'Nora', 60)")
        await db.commit()
        print("Database setup complete.")

async def asyncfetchusers(db):
    """
    Fetches all users from the database.
    """
    print("Starting to fetch ALL users...")
    await asyncio.sleep(0.5)
    async with db.execute("SELECT name, age FROM users") as cursor:
        results = await cursor.fetchall()
    print(f"Finished fetching ALL users ({len(results)} records).")
    return results


async def asyncfetcholder_users(db, age_limit=40):
    """
    Fetches users older than the specified age limit.
    """
    print(f"Starting to fetch users older than {age_limit}...")
    await asyncio.sleep(0.3)
    async with db.execute("SELECT name, age FROM users WHERE age > ?", (age_limit,)) as cursor:
        results = await cursor.fetchall()
    print(f"Finished fetching older users ({len(results)} records).")
    return results


async def fetch_concurrently():
    """
    Runs both query functions concurrently using asyncio.gather.
    """
    print("\n--- Starting Concurrent Fetching ---")
    
    async with aiosqlite.connect(DB_NAME) as db:
        # ✅ Call the correct snake_case functions
        all_users_task, older_users_task = await asyncio.gather(
            asyncfetchusers(db),
            asyncfetcholder_users(db)
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
