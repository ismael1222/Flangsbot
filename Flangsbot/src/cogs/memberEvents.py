from discord.ext.commands import Cog
from discord.embeds import Embed
from discord.member import Member

class MemberActions(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member):
        """
        TODO: Crear un sistema que permita obtener desde la base de datos
        el archivo de configuracion del servidor y retornar de el, el canal 
        de mensajes de bienvenida.
        """
        ch = self.bot.get_channel(722299537460559873) # Welcome Channel

        await ch.send(f'Bienvenido {member.mention}')

def setup(bot):
    bot.add_cog(MemberActions(bot))