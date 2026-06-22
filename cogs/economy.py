from discord.ext import commands
import discord

from config import DAILY_REWARD

from utils.database import (
    get_coins,
    add_coins,
    can_claim_daily,
    update_daily,
    get_top_coins,
    get_top_wins,
    get_top_winrate
)


class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # --------------------
    # BALANCE
    # --------------------

    @commands.command(name="balance")
    async def balance(self, ctx):

        coins = await get_coins(ctx.author.id)

        embed = discord.Embed(
            title="💰 Balance",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="Coins",
            value=f"{coins:,}",
            inline=False
        )

        await ctx.send(embed=embed)

    # --------------------
    # DAILY
    # --------------------

    @commands.command(name="daily")
    async def daily(self, ctx):

        allowed = await can_claim_daily(ctx.author.id)

        if not allowed:

            embed = discord.Embed(
                title="❌ Daily Already Claimed",
                description="Come back in 12 hours.",
                color=discord.Color.red()
            )

            return await ctx.send(embed=embed)

        await add_coins(
            ctx.author.id,
            DAILY_REWARD
        )

        await update_daily(
            ctx.author.id
        )

        embed = discord.Embed(
            title="🎁 Daily Reward",
            description=f"+{DAILY_REWARD} Coins",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

    # --------------------
    # TOP COINS
    # --------------------

    @commands.command(name="top")
    async def top(self, ctx):

        leaderboard = await get_top_coins()

        embed = discord.Embed(
            title="🏆 Richest Players",
            color=discord.Color.gold()
        )

        text = ""

        for pos, data in enumerate(leaderboard, start=1):

            user_id, coins = data

            user = self.bot.get_user(user_id)

            if user:
                name = user.name
            else:
                name = f"User {user_id}"

            text += (
                f"**#{pos}** "
                f"{name} — "
                f"{coins:,} Coins\n"
            )

        embed.description = text

        await ctx.send(embed=embed)

    # --------------------
    # TOP WINS
    # --------------------

    @commands.command(name="topwins")
    async def topwins(self, ctx):

        leaderboard = await get_top_wins()

        embed = discord.Embed(
            title="🏆 Most Wins",
            color=discord.Color.blue()
        )

        text = ""

        for pos, data in enumerate(leaderboard, start=1):

            user_id, wins = data

            user = self.bot.get_user(user_id)

            if user:
                name = user.name
            else:
                name = f"User {user_id}"

            text += (
                f"**#{pos}** "
                f"{name} — "
                f"{wins} Wins\n"
            )

        embed.description = text

        await ctx.send(embed=embed)

    # --------------------
    # TOP WINRATE
    # --------------------

    @commands.command(name="topwinrate")
    async def topwinrate(self, ctx):

        leaderboard = await get_top_winrate()

        embed = discord.Embed(
            title="🏆 Best Win Rate",
            color=discord.Color.purple()
        )

        text = ""

        for pos, data in enumerate(
            leaderboard,
            start=1
        ):

            user_id, rate = data

            user = self.bot.get_user(user_id)

            if user:
                name = user.name
            else:
                name = f"User {user_id}"

            text += (
                f"**#{pos}** "
                f"{name} — "
                f"{rate}%\n"
            )

        embed.description = text

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Economy(bot))
