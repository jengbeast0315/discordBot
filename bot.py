import discord
import os
from discord.ext import commands

# Load bot token from environment variable
TOKEN = os.getenv("TOKEN")  # Now reads token from environment

intents = discord.Intents.default()
intents.message_content = True  # Allows reading message content

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def racist(ctx):
    await ctx.send("niggers")

# Run the bot
bot.run(TOKEN)
