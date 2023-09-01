"""bot.py"""
import os
import discord
from discord.ext import commands
from pymongo import MongoClient
import config

TOKEN = config.TOKEN
intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix='$', intents=intent)
bot.remove_command("help")

client = MongoClient(config.MONGODB)
db = client.user_oshi

async def load():
    """
    Loads commands from the commands folder
    """
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            await bot.load_extension(f"commands.{filename[:-3]}")

@bot.group(invoke_without_command=True)
async def help(ctx):
    """
    Replaces the current help command with an embeded help command
    """
    msg = discord.Embed(title="HELP", description="Use $help <command> for extended details")

    msg.add_field(name="General", value="anystreams, stream")
    msg.add_field(name="Oshi", value="oshiadd, oshidel, oshilist, oshistreams")

    await ctx.send(embed=msg)

@help.command()
async def anystreams(ctx):
    """
    Brief description of the functionality and usage of $anystreams
    """
    msg = discord.Embed(
        title="$anystreams",
        description="Displays all upcoming/current Hololive streams"
        )

    msg.add_field(name="Format", value="$anystreams <limit> [default = 5, upper limit = 20]")

    await ctx.send(embed=msg)

@help.command()
async def stream(ctx):
    """
    Brief description of the functionality and usage of $stream
    """
    msg = discord.Embed(
        title="$stream",
        description="Displays upcoming/current streams of a specific Hololive Vtuber"
        )

    msg.add_field(name="Format", value="$stream <vtuber>")

    await ctx.send(embed=msg)

@help.command()
async def oshiadd(ctx):
    """
    Brief description of the functionality and usage of $oshiadd
    """
    msg = discord.Embed(
        title="$oshiadd",
        description="Adds one of your oshi into your personal list"
        )

    msg.add_field(name="Format", value="$oshiadd <vtuber>")

    await ctx.send(embed=msg)

@help.command()
async def oshidel(ctx):
    """
    Brief description of the functionality and usage of $oshidel
    """
    msg = discord.Embed(
        title="$oshidel",
        description="Deletes one of your oshi from your personal list"
        )

    msg.add_field(name="Format", value="$oshidel <vtuber>")

    await ctx.send(embed=msg)

@help.command()
async def oshilist(ctx):
    """
    Brief description of the functionality and usage of $oshilist
    """
    msg = discord.Embed(
        title="$oshilist",
        description="Displays all of your saved oshi"
        )

    msg.add_field(name="Format", value="$oshilist")

    await ctx.send(embed=msg)

@help.command()
async def oshistreams(ctx):
    """
    Brief description of the functionality and usage of $oshistreams
    """
    msg = discord.Embed(
        title="$oshistreams",
        description="Displays upcoming/current streams of your oshi"
        )

    msg.add_field(name="Format", value="$oshisteams")

    await ctx.send(embed=msg)

@bot.event
async def on_ready():
    """
    Message to confirm that HoloBot has connected to Discord
    """
    print(f'{bot.user.name} is connected to Discord!')

async def main():
    """
    Loads and starts the discord bot
    """
    async with bot:
        await load()
        await bot.start(TOKEN)
