from discord.ext.commands.core import command
from lib import bot
from discord.errors import DiscordException
from discord.ext.commands import Cog
from discord.ext.commands.errors import *
from discord.errors import *

class SuperCommand(Cog):
    def __init__(self):
        self.bot = bot
    
    @command(name="spc")
    async def spc(self, ctx):
        pass

    """
    Muestra partes del codigo del bot
    Se requiere de ciertos permisos del server
    """