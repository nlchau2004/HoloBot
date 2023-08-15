"""bot.py"""
import discord
from discord.ext import commands
import api
import config

TOKEN = config.TOKEN
intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix='!', intents=intent)


@bot.event
async def on_ready():
    """
    Notifies the terminal whether it's connected to Discord or not
    """
    print(f'{bot.user.name} is connected to Discord!')


@bot.command(name='streams', help="Responds with all upcoming Hololive streams")
async def all_upcoming_streams(ctx):
    """
    Sends a message containing all the upcoming streams including:
    Title
    Vtuber Name
    Time
    """
    streams = api.get_streams()
    oshi = [s["channel"]["english_name"] for s in streams]
    upcoming = api.parse_streams(streams, oshi)
    for vtuber, stream in upcoming.items():
        await ctx.send(f"{vtuber}: {stream['stream']}")


bot.run(TOKEN)
