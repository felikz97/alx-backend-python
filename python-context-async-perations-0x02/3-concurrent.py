import asyncio
import aiosqlite

async def setup_database():
    async with aiosqlite.connect("test_async.db") as db:
        await db.execute("DROP TABLE IF EXISTS users")
        await db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
        users = [
            ("Felikz", 24), ("Jamine", 30), ("Duke", 45),
            ("David", 22), ("Sylvia", 50), ("Frank", 41)
        ]
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users)
        await db.commit()

async def async_fetch_users():
    async with aiosqlite.connect("test_async.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users():
    async with aiosqlite.connect("test_async.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()

async def fetch_concurrently():
    await setup_database()
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All Users:", all_users)
    print("Users older than 40:", older_users)

# Entry point
asyncio.run(fetch_concurrently())
