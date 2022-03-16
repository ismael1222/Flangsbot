from discord.ext.commands import Cog, command, has_permissions

from Flangsbot.src.db.models.Guild import GuildTable
from aiosqlite import connect

class Database(Cog, name="Database manager", description="Manages the database"):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(administrator=True)
    @command(name = 'db')
    async def database(self, ctx, *args, **kargs):
        conn = await connect('Flangsbot/src/db/database.db')
        await ctx.send(f'Connection to database established. [{type(conn)}]')
        await GuildTable(conn, ctx.guild.id).create_guild()
        await ctx.send(f'Guild database created as ``Guild_{ctx.guild.id}``.')

def setup(bot):
    bot.add_cog(Database(bot))