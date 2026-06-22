import aiosqlite
import time

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


# ----------------------------
# USER FUNCTIONS
# ----------------------------

async def create_user(user_id: int):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            "SELECT user_id FROM users WHERE user_id = ?",
            (user_id,)
        )

        user = await cursor.fetchone()

        if not user:

            await db.execute(
                "INSERT INTO users(user_id) VALUES(?)",
                (user_id,)
            )

            await db.commit()


async def get_user(user_id: int):

    await create_user(user_id)

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )

        return await cursor.fetchone()


# ----------------------------
# COINS
# ----------------------------

async def get_coins(user_id: int):

    user = await get_user(user_id)

    return user[1]


async def add_coins(user_id: int, amount: int):

    await create_user(user_id)

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            "UPDATE users SET coins = coins + ? WHERE user_id = ?",
            (amount, user_id)
        )

        await db.commit()


async def remove_coins(user_id: int, amount: int):

    await create_user(user_id)

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            "UPDATE users SET coins = MAX(coins - ?, 0) WHERE user_id = ?",
            (amount, user_id)
        )

        await db.commit()


# ----------------------------
# DAILY
# ----------------------------

async def can_claim_daily(user_id: int):

    user = await get_user(user_id)

    last_daily = user[7]

    now = int(time.time())

    return now - last_daily >= 43200


async def update_daily(user_id: int):

    now = int(time.time())

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute(
            "UPDATE users SET last_daily = ? WHERE user_id = ?",
            (now, user_id)
        )

        await db.commit()


# ----------------------------
# STATS
# ----------------------------

async def add_win(user_id: int):

    await create_user(user_id)

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        UPDATE users
        SET wins = wins + 1,
            games_played = games_played + 1
        WHERE user_id = ?
        """, (user_id,))

        await db.commit()


async def add_loss(user_id: int):

    await create_user(user_id)

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        UPDATE users
        SET losses = losses + 1,
            games_played = games_played + 1
        WHERE user_id = ?
        """, (user_id,))

        await db.commit()


async def add_spy_win(user_id: int):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        UPDATE users
        SET spy_wins = spy_wins + 1
        WHERE user_id = ?
        """, (user_id,))

        await db.commit()


async def add_villager_win(user_id: int):

    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        UPDATE users
        SET villager_wins = villager_wins + 1
        WHERE user_id = ?
        """, (user_id,))

        await db.commit()


# ----------------------------
# LEADERBOARDS
# ----------------------------

async def get_top_coins(limit=10):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
        SELECT user_id, coins
        FROM users
        ORDER BY coins DESC
        LIMIT ?
        """, (limit,))

        return await cursor.fetchall()


async def get_top_wins(limit=10):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
        SELECT user_id, wins
        FROM users
        ORDER BY wins DESC
        LIMIT ?
        """, (limit,))

        return await cursor.fetchall()


async def get_top_winrate(limit=10):

    async with aiosqlite.connect(DATABASE) as db:

        cursor = await db.execute("""
        SELECT
        user_id,
        wins,
        games_played
        FROM users
        WHERE games_played > 0
        """)

        users = await cursor.fetchall()

    leaderboard = []

    for user_id, wins, games in users:

        rate = (wins / games) * 100

        leaderboard.append(
            (user_id, round(rate, 2))
        )

    leaderboard.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return leaderboard[:limit]
