"""bot.py"""
import discord
from dotenv import load_dotenv
import config

load_dotenv()
TOKEN = config.TOKEN

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    """
    Notifies client about successful connection to Discord
    along with servers the bot it's connected to
    """
    for guild in client.guilds:
        if guild.name == config.GUILD:
            break

    print(f'{client.user} has connected to Discord!')
    print(f'{client.user} is connected to {guild.name}: {guild.id}')

client.run(TOKEN)
