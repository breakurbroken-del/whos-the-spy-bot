import aiosqlite

DATABASE = "database/bot.db"

async def setup_database():
    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            coins INTEGER DEFAULT 1000,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            games_played INTEGER DEFAULT 0,
            spy_wins INTEGER DEFAULT 0,
            villager_wins INTEGER DEFAULT 0,
            last_daily INTEGER DEFAULT 0
        )
        """)

        await db.commit()
