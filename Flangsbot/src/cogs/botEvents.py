import discord
from discord.ext.commands import Cog

class EventHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity= discord.Game(
                name=f'$ | Servers: {self.bot.guilds}'
            )
        )

def setup(bot):
    bot.add_cog(EventHandler(bot))