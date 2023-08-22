"""embed.py"""
from datetime import datetime
from datetime import timezone
import discord

class EmbedMessage:
    """
    Object that represents the embed messages that will be
    sent to the user.
    """
    def __init__(self, vtuber:str, streams: dict) -> None:
        """
        When initialized, the object requires:
        Vtuber's name
        Their upcoming/live streams
        """
        self.vtuber = vtuber
        self.stream = streams[vtuber]
        self.message = None

    def create_message(self, author) -> None:
        """
        Creates an embed message and assigns that object to
        the message value
        """
        self.message = discord.Embed(
            title=self.stream["stream"],
            colour=discord.Colour.random()
            )

        self.message.set_author(
            name=self.vtuber,
            icon_url=self.stream["image"]
            )

        self.message.set_thumbnail(url=self.stream["image"])

        self.message.add_field(
            name="Link",
            value=f"https://www.youtube.com/watch?v={self.stream['link']}",
            inline=False
        )

        self.message.add_field(
            name="Scheduled Time", value=self.generate_time(self.stream["scheduled_time"])
            )

        self.message.set_footer(text=f"Information requested by: {author}")

    def generate_time(self, time: str) -> str:
        """
        Given a string of raw time, the method will convert
        the raw input into a sensible unit of time
        """
        time = datetime.fromisoformat(self.stream["scheduled_time"][:-1]).astimezone(timezone.utc)
        return time
