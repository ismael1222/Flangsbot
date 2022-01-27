import discord, random
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands.errors import BadArgument, MissingRequiredArgument
from discord.errors import Forbidden

def get_presence() -> str:
    PRESENCES = [
        "None",
        "Algo",
        "Nose",
        "Lets fucking go",
        "Lets go",
        "Destroy",
        "Yeah",
        "Error 404: Not Found"
    ]
    return random.choice(PRESENCES)

class EventHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ch = self.bot.get_channel(722299537460559873)
    
    @Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity= discord.Game(
                name= get_presence()
            )
        )

def setup(bot):
    bot.add_cog(EventHandler(bot))