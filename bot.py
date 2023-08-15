"""bot.py"""
import discord
from discord.ext import commands
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


@bot.command(name='hi')
async def hi(ctx):
    """
    Prototype function that tests the functionality
    of HoloBot's messages
    """
    await ctx.send('Hi!')

bot.run(TOKEN)
