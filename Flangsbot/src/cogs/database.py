from discord.ext.commands import Cog, command
from discord.embeds import Embed

from aiosqlite import connect

from Flangsbot.src.db.manager import DataBaseManager
from Flangsbot.src.db.models.Guild import GuildMDB

class Database(Cog, name="Database manager", description="Manages the database"):
    def __init__(self, bot):
        self.bot = bot

    @command(name = 'db')
    async def database(self, ctx, *args, **kargs):
        conn = await connect('Flangsbot/src/db/database.db')

        db = DataBaseManager.db_type(conn)

        GuildMDB(db, ctx.guild.id).create_guild()

def setup(bot):
    bot.add_cog(Database(bot))