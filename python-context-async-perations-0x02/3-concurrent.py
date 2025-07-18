#!/usr/bin/env python3
import asyncio
import aiosqlite

DB_PATH = "users.db"  # make sure your SQLite DB is named correctly

async def async_fetch_users():
    """Asynchronously fetch all users from the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            print("All Users:")
            for row in rows:
                print(row)
            return rows

async def async_fetch_older_users():
    """Asynchronously fetch users older than 40."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            print("\nUsers Older Than 40:")
            for row in rows:
                print(row)
            return rows

async def fetch_concurrently():
    """Run both fetch functions concurrently."""
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
