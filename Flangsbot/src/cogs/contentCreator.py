from discord.ext.commands import Cog, command, cooldown, BucketType

from discord_components import Button, ButtonStyle, Select, SelectOption, component, interaction

class ContentCreator(Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    NOTE: El sistema se basa en que los usuarios con roles destacados puedan crear sus propios canales donde hablar acerca de un tema en espesifico.
        * Primero. Para evitar acumulacion de temas similares, los moderadores (default) deveran aceptar los tikets de verificacion.
        * Segundo. Los usuarios estaran clasificados en ordenes de prioridad, de mayor a menor. Aquellos con mayor jerarquia tendran mayores posibilidades de crear canales.
            + Roles como "Wumpus" tendran mayor capacidad de crear canales con diferentes temas. (Mayor nivel mas canales disponibles)
        * Tercero. Todos los usuarios sin esepcion ganaran experiencia por participar en los canales, la cual podra ser cangeable por roles prestigiosos.

    TODO: Utilizar DiscordComponents para crear interfaces de usuario.


    FLAN:
        * $channel manage 
            + $channel manage rename <nombre>
            + $channel manage theme <tema>
            + $channel manage delete
            + $channel manage add_role
            + $channel manage remove_role
    """

    # @command(name = 'tickch')
    # async def ticket(self, ctx, objec: str):
    #     pass

    @command(name = 'channel')
    async def channel(self, ctx, *args, **kargs):
        pass

    # @command(name = 'crch')
    # async def create_channel(self, ctx, name: str, *theme: str):
    #     pass

    # @command(name = 'rmch')
    # async def delete_channel(self, ctx, id: str):
    #     pass

    # @command(name = 'synch')
    # async def sync_channels(self, ctx, id: str):
    #     pass

def setup(bot):
    bot.add_cog(ContentCreator(bot))