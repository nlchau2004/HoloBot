"""bot.py"""
import discord
from discord.ext import commands
import embed
import api
import config

TOKEN = config.TOKEN
intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix='$', intents=intent)
bot.remove_command("help")

@bot.group(invoke_without_command=True)
async def help(ctx):
    """
    Replaces the current help command with an embeded help command
    """
    msg = discord.Embed(title="HELP", description="Use $help <command> for extended details")

    msg.add_field(name="Commands", value="anystreams, stream")

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

@bot.event
async def on_ready():
    """
    Message to confirm that HoloBot has connected to Discord
    """
    print(f'{bot.user.name} is connected to Discord!')

@bot.event
async def on_command_error(ctx, error):
    """
    Triggers when an error occurs during a command
    """
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("That command wasn't found! Sorry :(")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("Invalid argument, please try again")

@bot.command(
        name='anystreams',
        )
async def all_streams(ctx, limit=5):
    """
    Sends a message containing all the upcoming streams including:
    Title
    Vtuber Name
    Time

    The default limit of streams is 5, while the upper limit is 20
    (This may be subject to change in the future)
    """

    try:
        assert limit < 20
        streams = api.get_streams()
        oshi = [s["channel"]["english_name"] for s in streams]
        upcoming = api.parse_streams(streams, oshi)
        for i in range(limit):
            vtuber = oshi[i]
            message = embed.EmbedMessage(vtuber, upcoming)
            message.create_message(ctx.author.display_name)
            await ctx.send(embed=message.message)
        await ctx.send(f"Here you go {ctx.message.author.mention}!")
    except AssertionError:
        await ctx.send("Woah! Too many streams at one time!")

@bot.command(
        name='stream',
        )
async def vtuber_streams(ctx, vtuber:str=None):
    """
    Unlike all_streams, this will only return streams from a given Hololive Vtuber
    
    User must provide a specific Vtuber
    """
    if not isinstance(vtuber, str):
        raise discord.ext.commands.errors.BadArgument

    streams = api.get_streams()
    upcoming = api.parse_streams(streams, [vtuber])
    message = embed.EmbedMessage(vtuber, upcoming)
    message.create_message(ctx.author.display_name)
    await ctx.send(embed=message.message)
    await ctx.send(f"Here you go {ctx.message.author.mention}!")

def run_bot():
    """
    Runs the discord bot
    """
    bot.run(TOKEN)
