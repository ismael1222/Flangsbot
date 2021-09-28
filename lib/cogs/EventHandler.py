from ..db import db
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands.errors import BadArgument, MissingRequiredArgument
from discord.errors import Forbidden

class EventHandler(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ch = self.bot.get_channel(722299537460559873)
        

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)

        await self.ch.send("Bienvenid@")

        try:
            await member.send("Bienvenid@")
            await member.add_roles(member.guild.get_role(651235495870988288))

        except Forbidden:
            pass

    @Cog.listener()
    async def on_member_remove(self, member):
        pass

def setup(bot):
    bot.add_cog(EventHandler(bot))