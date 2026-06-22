from discord.ext import commands
import discord

from utils.database import get_user


class Profile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="profile")
    async def profile(self, ctx, member: discord.Member = None):

        if member is None:
            member = ctx.author

        user = await get_user(member.id)

        coins = user[1]
        wins = user[2]
        losses = user[3]
        games_played = user[4]
        spy_wins = user[5]
        villager_wins = user[6]

        if games_played > 0:
            win_rate = round(
                (wins / games_played) * 100,
                2
            )
        else:
            win_rate = 0

        embed = discord.Embed(
            title="👤 Player Profile",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Name",
            value=member.name,
            inline=False
        )

        embed.add_field(
            name="User ID",
            value=member.id,
            inline=False
        )

        embed.add_field(
            name="Coins",
            value=f"{coins:,}",
            inline=True
        )

        embed.add_field(
            name="Wins",
            value=wins,
            inline=True
        )

        embed.add_field(
            name="Losses",
            value=losses,
            inline=True
        )

        embed.add_field(
            name="Games Played",
            value=games_played,
            inline=True
        )

        embed.add_field(
            name="Win Rate",
            value=f"{win_rate}%",
            inline=True
        )

        embed.add_field(
            name="Spy Wins",
            value=spy_wins,
            inline=True
        )

        embed.add_field(
            name="Villager Wins",
            value=villager_wins,
            inline=True
        )

        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Profile(bot))
