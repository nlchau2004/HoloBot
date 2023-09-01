"""oshi.py"""
import secrets
import discord
from discord.ext import commands
from pymongo import MongoClient
import api
import embed
import config


class Oshi(commands.Cog):
    """
    Class that focuses on handling a user's oshi and their list.
    This class also contains the commands that pertain to oshi such as:

    oshiadd
    oshidel
    oshilist
    oshistreams
    """
    def __init__(self, bot):
        """
        When initialized, the class will generate a database collection for
        usage and list of all channels under the Hololive name
        """
        self.bot = bot
        self.client = MongoClient(config.MONGODB)
        self.database = self.client.user_info
        self.holomems = [vtuber["english_name"] for vtuber in api.get_channels()]

    @commands.command(name="oshiadd")
    async def add_oshi(self, ctx, oshi:str=None):
        """
        Adds an oshi to the user's list
        If the oshi does not exist or provides an empty prompt,
        a BadArgument error is raised
        """
        if not isinstance(oshi, str):
            raise discord.ext.commands.errors.BadArgument

        if oshi in self.holomems:
            author = ctx.author.id
            key = {"author": author}

            data = {
                "oshi": oshi
            }

            user_info = {f'ticket_id.{secrets.token_hex(6)}': data}
            self.database.oshi.update_one(
                key,
                {"$set": user_info},
                True
            )
            await ctx.send("Oshi has been successfully added!")
        else:
            raise discord.ext.commands.errors.BadArgument

    @commands.command(name="oshidel")
    async def del_oshi(self, ctx, oshi:str=None):
        """
        Deletes a oshi from the user's list
        If the oshi does not exist or provides an empty prompt,
        a BadArgument error is raised
        """
        if (not isinstance(oshi, str)) or not(oshi in self.holomems):
            raise discord.ext.commands.errors.BadArgument

        user = self.database.oshi.find_one({"author": ctx.author.id})
        for mem in user["ticket_id"]:
            vtuber = user["ticket_id"][mem]["oshi"]
            if vtuber == oshi:
                ticket_id = "ticket_id." + mem
                self.database.oshi.update_one(
                    {},
                    {"$unset": {ticket_id: None}}
                    )
        await ctx.send("Oshi has been successfully deleted!")

    @commands.command("oshilist")
    async def oshi_list(self, ctx):
        """
        Displays the list of the user's oshi
        """
        oshi_list = discord.Embed(
            title="List of Oshi",
            colour=discord.Colour.random()
            )
        user = self.database.oshi.find_one({"author": ctx.author.id})
        for oshi in user["ticket_id"]:
            for info in api.get_channels():
                vtuber = user["ticket_id"][oshi]["oshi"]
                if info["english_name"] == vtuber:
                    oshi_list.add_field(
                        name=vtuber,
                        value=f"https://www.youtube.com/channel/{info['id']}",
                        inline=False
                        )
        await ctx.send(embed=oshi_list)

    @commands.command("oshistreams")
    async def oshi_streams(self, ctx):
        """
        Displays all streams of Hololive members that a user has
        saved into their oshi list
        """
        streams = api.get_streams()
        oshi = []
        user = self.database.oshi.find_one({"author": ctx.author.id})
        for mem in user["ticket_id"]:
            vtuber = user["ticket_id"][mem]["oshi"]
            oshi.append(vtuber)
        upcoming = api.parse_streams(streams, oshi)
        for vtuber in oshi:
            message = embed.EmbedMessage(vtuber, upcoming)
            message.create_message(ctx.author.display_name)
            await ctx.send(embed=message.message)
        await ctx.send(f"Here you go {ctx.message.author.mention}!")

async def setup(bot):
    await bot.add_cog(Oshi(bot))
