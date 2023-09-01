"""streams.py"""
import discord
from discord.ext import commands
import embed
import api


class DisplayStreams(commands.Cog):
    """
    DisplayStreams handles all the commands that focus on displaying
    embed messages that contain streaming information, with the
    exception of streams from a user's oshi (singular or plural).
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Triggers when an error occurs during a command
        """
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            await ctx.send("That command wasn't found! Sorry :(")
        elif isinstance(error, discord.ext.commands.errors.BadArgument):
            await ctx.send("Invalid argument, please try again")

    @commands.command(name="anystreams")
    async def all_streams(self, ctx, limit=5):
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

    @commands.command(name="stream")
    async def vtuber_streams(self, ctx, vtuber:str=None):
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


async def setup(bot):
    await bot.add_cog(DisplayStreams(bot))