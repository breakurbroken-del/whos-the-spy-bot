import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.database import setup_database

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="-",
    intents=intents
)

@bot.event
async def on_ready():

    await setup_database()

    print(f"{bot.user} is online")

    await bot.load_extension("cogs.economy")
    await bot.load_extension("cogs.profile")
    await bot.load_extension("cogs.game")

bot.run(TOKEN)
