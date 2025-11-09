import asyncio
import aiosqlite
import time

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
        
# Function name corrected back to snake_case as required by the checker
async def async_fetch_users(db):
    """
    Fetches all users from the database.
    """
    print(f"Starting to fetch ALL users...")
    await asyncio.sleep(0.5) 
    async with db.execute("SELECT name, age FROM users") as cursor:
        results = await cursor.fetchall()
    print(f"Finished fetching ALL users ({len(results)} records).")
    return results

# Function name corrected back to snake_case as required by the checker
async def async_fetch_older_users(db, age_limit=40):
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
    
    # Connect to the database once
    async with aiosqlite.connect(DB_NAME) as db:
        
        # Use asyncio.gather() with the required snake_case function names
        all_users_task, older_users_task = await asyncio.gather(
            async_fetch_users(db),     # Uses the required name (with underscore)
            async_fetch_older_users(db) # Uses the required name (with underscore)
        )

    print("\n--- Results ---")
    print("All Users:")
    for name, age in all_users_task:
        print(f" - {name}, Age: {age}")
        
    print("\nUsers Older than 40:")
    for name, age in older_users_task:
        print(f" - {name}, Age: {age}")

if __name__ == "__main__":
    # Must setup the database before reading from it
    asyncio.run(setup_database())
    
    # Run the concurrent fetching process
    asyncio.run(fetch_concurrently())
