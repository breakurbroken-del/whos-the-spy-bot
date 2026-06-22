from views.ready_view import ReadyView

from discord.ext import commands
import discord
import asyncio

from config import (
    MIN_PLAYERS,
    MAX_PLAYERS,
    ENTRY_COST,
    MAX_ACTIVE_GAMES
)

from utils.sessions import (
    active_games,
    create_session,
    session_exists,
    remove_session
)

from utils.database import (
    get_coins,
    remove_coins
)
import random

from utils.words import get_random_words

class Game(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="start")
    async def start_game(self, ctx):

        # Must be in VC
        if not ctx.author.voice:

            embed = discord.Embed(
                title="❌ Error",
                description="You must be in a Voice Channel.",
                color=discord.Color.red()
            )

            return await ctx.send(embed=embed)

        vc = ctx.author.voice.channel

        # Active game check
        if session_exists(vc.id):

            embed = discord.Embed(
                title="❌ Error",
                description="A game is already running in this Voice Channel.",
                color=discord.Color.red()
            )

            return await ctx.send(embed=embed)

        # Global limit
        if len(active_games) >= MAX_ACTIVE_GAMES:

            embed = discord.Embed(
                title="❌ Error",
                description="Maximum active games reached.",
                color=discord.Color.red()
            )

            return await ctx.send(embed=embed)

        members = [
            m for m in vc.members
            if not m.bot
        ]

        # Player count
        if len(members) < MIN_PLAYERS:

            embed = discord.Embed(
                title="❌ Not Enough Players",
                description=f"Minimum {MIN_PLAYERS} players required.",
                color=discord.Color.red()
            )

            return await ctx.send(embed=embed)

        if len(members) > MAX_PLAYERS:

            embed = discord.Embed(
                title="❌ Too Many Players",
                description=f"Maximum {MAX_PLAYERS} players allowed.",
                color=discord.Color.red()
            )

            return await ctx.send(embed=embed)

        # Coin check
        low_coin_players = []

        for member in members:

            coins = await get_coins(member.id)

            if coins < ENTRY_COST:

                low_coin_players.append(
                    member.mention
                )

        if low_coin_players:

            embed = discord.Embed(
                title="❌ Not Enough Coins",
                color=discord.Color.red()
            )

            embed.description = "\n".join(
                low_coin_players
            )

            embed.add_field(
                name="Required",
                value=f"{ENTRY_COST} Coins"
            )

            return await ctx.send(
                embed=embed
            )

        # Create Session
        session = create_session(
            guild_id=ctx.guild.id,
            vc_id=vc.id,
            text_channel_id=ctx.channel.id,
            host_id=ctx.author.id
        )

        session.players = [
            member.id
            for member in members
        ]

        # Lobby Embed
        embed = discord.Embed(
            title="🎭 Who's The Spy",
            description="Lobby Created",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Voice Channel",
            value=vc.name,
            inline=False
        )

        embed.add_field(
            name="Players",
            value=f"{len(members)}/{MAX_PLAYERS}",
            inline=False
        )

        embed.add_field(
            name="Host",
            value=ctx.author.mention,
            inline=False
        )

        embed.set_footer(
            text="Click Ready To Continue"
        )

        view = ReadyView(session)

        await ctx.send(
            embed=embed,
            view=view
        )

        await view.wait()

        if len(session.ready_players) != len(session.players):

            from utils.sessions import remove_session

            remove_session(vc.id)

            await ctx.send(
                "❌ Lobby Cancelled."
            )

            return

        await ctx.send(
            "✅ Everyone Is Ready!"
        )

        # Select Spy

        session.spy_id = random.choice(
            session.players
        )

        # Generate Words

        word_data = get_random_words()

        session.villager_word = (
            word_data["villager_word"]
        )

        session.spy_word = (
            word_data["spy_word"]
        )

        failed_dm = []

        for player_id in session.players:

            member = ctx.guild.get_member(
                player_id
            )

            try:

                if player_id == session.spy_id:

                    embed = discord.Embed(
                        title="🕵️ Spy",
                        color=discord.Color.red()
                    )

                    embed.add_field(
                        name="Your Word",
                        value=session.spy_word,
                        inline=False
                    )

                else:

                    embed = discord.Embed(
                        title="🏡 Villager",
                        color=discord.Color.green()
                    )

                    embed.add_field(
                        name="Your Word",
                        value=session.villager_word,
                        inline=False
                    )

                embed.add_field(
                    name="Voice Channel",
                    value=vc.name,
                    inline=False
                )

                await member.send(
                    embed=embed
                )

            except Exception:

                failed_dm.append(
                    member.mention
                )

        if failed_dm:

            remove_session(vc.id)

            await ctx.send(
                "❌ DM Failed For:\n"
                + "\n".join(failed_dm)
            )

            return

        # Deduct Entry Fee

        for player_id in session.players:

            await remove_coins(
                player_id,
                ENTRY_COST
            )

        await ctx.send(
            f"💰 {ENTRY_COST} Coins Deducted From All Players."
        )

        # Lock Voice Channel

        everyone_role = ctx.guild.default_role

        await vc.set_permissions(
            everyone_role,
            connect=False
        )

        await ctx.send(
            "🔒 Voice Channel Locked."
        )
        
        # Mute Everyone

        for member in vc.members:

            if not member.bot:

                try:

                    await member.edit(
                        mute=True
                    )

                except Exception:
                    pass

        await ctx.send(
            "🔇 Everyone Has Been Muted."
        )
        
        await ctx.send(
            "📩 Roles Sent Successfully!"
        )
        # Speaking Queue

        session.speaking_queue = [
            player_id
            for player_id in session.players
        ]

        embed = discord.Embed(
            title="🎤 Round 1",
            description="Speaking Phase Started",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="Players",
            value=str(
                len(session.speaking_queue)
            ),
            inline=False
        )

        embed.add_field(
            name="Time Per Player",
            value="15 Seconds",
            inline=False
        )

        embed.set_footer(
            text=vc.name
        )

        await ctx.send(
            embed=embed
        )

        for player_id in session.speaking_queue:

            if player_id in session.eliminated_players:
                continue

            member = ctx.guild.get_member(
                player_id
            )

            if not member:
                continue

            await ctx.send(
                f"🎤 {member.mention} Your Turn\n"
                "You Have 15 Seconds."
            )

            try:

                await member.edit(
                    mute=False
                )

            except Exception:
                pass

            await asyncio.sleep(15)

            try:

                await member.edit(
                    mute=True
                )

            except Exception:
                pass

            await ctx.send(
                f"🔇 {member.mention} Finished."
            )

        await ctx.send(
            "🗳️ Voting Phase Coming Soon."
        )
        
async def setup(bot):
    await bot.add_cog(Game(bot))
