import discord
import asyncio
import yt_dlp
import os
from discord.ext import commands
from discord import FFmpegPCMAudio

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

@bot.command()
async def join(ctx):
    """Bot joins the voice channel of the user who invoked the command."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"🎵 Joined {channel.name}!")
    else:
        await ctx.send("❌ You must be in a voice channel first!")

@bot.command()
async def leave(ctx):
    """Bot leaves the voice channel."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the voice channel!")
    else:
        await ctx.send("❌ I'm not in a voice channel!")

@bot.command()
async def play(ctx, url: str):
    """Plays audio from a YouTube video in a voice channel."""
    if not ctx.voice_client:
        await join(ctx)  # Auto-join if not in a voice channel

    await ctx.send(f"🔍 Fetching audio from: {url}")

    # YouTube download options
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'song.mp3',
        'quiet': True
    }

    # Download audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Play audio
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()

    source = FFmpegPCMAudio("song.mp3")
    voice_client.play(source, after=lambda e: print("Finished playing."))

    await ctx.send("🎶 Now playing!")

@bot.command()
async def stop(ctx):
    """Stops the current audio."""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹ Stopped playing.")
    else:
        await ctx.send("❌ No audio is playing!")

bot.run(TOKEN)
