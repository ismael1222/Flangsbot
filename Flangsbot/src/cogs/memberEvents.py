from typing import Dict

from discord.ext.commands import Cog
from discord.embeds import Embed
from discord.member import Member

class WelcomeActions(Cog):
    def __init__(self, bot):
        self.bot = bot
        #FIX: Change this for a database model.
        self.welcome_channels: Dict[int, int] = {
            651231834356711427: 722299537460559873, #Flangscom
            804500094686330912: 805180994117697557, #Survivaland
        }

    @Cog.listener()
    async def on_member_join(self, member: Member):
        #TODO: Make a module that checks if the guild has in the database. 
        # If the guild isn't in the database, it will create a new table. 
        # If the guild it's in the database, it will return the default welcome channel.

        guild = member.guild
        guild_id = member.guild.id

        #FIX: Change this for a database model.
        channel = self.bot.get_channel(
            self.welcome_channels[guild_id]
        )

        embed = Embed(
            title = "Welcome to the server!",
            description = "Welcome to {} {}".format(guild.name, member.mention),
            color = 0x00ff00
        )

        await channel.send(embed)

        #NOTE: Givear desde la base de datos el canal de bienvenida segun el guild.
        #NOTE: Si el guild donde ingreso el usuario no tiene un canal de bienvenida por defecto configurado, raisear un error.

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        guild = member.guild
        guild_id = member.guild.id

        #FIX: Change this for a database model.
        channel = self.bot.get_channel(
            self.welcome_channels[guild_id]
        )

        await channel.send(f"{member.mention} has left the server.")

def setup(bot):
    bot.add_cog(WelcomeActions(bot))