from typing import Dict
from aiosqlite import connect

from discord.ext.commands import Cog, Bot
from discord.embeds import Embed
from discord.member import Member

from Flangsbot.src.db.models.Guild import TableGuild

class WelcomeActions(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

#FIX: RuntimeWarning: coroutine 'SqliteDatabase.with_cursor.<locals>.inner' was never awaited.
#TODO: Create a system that will send custom welcome message to the user from database.
    @Cog.listener()
    async def on_member_join(self, member: Member):
        conn = await connect('Flangsbot/src/db/database.db')
        guild_id = member.guild.id

        result: Dict[str, int] = await TableGuild(conn, guild_id).select_one_where(
            keys = "welcome_channel_id",
            checks = {'id' : guild_id}
        )

        channel = self.bot.get_channel(
            result["welcome_channel_id"]
        )

        await channel.send(f'{member.mention} has joined the server!')

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        conn = await connect('Flangsbot/src/db/database.db')
        guild_id = member.guild.id

        result: Dict[str, int] = await TableGuild(conn, guild_id).select_one_where(
            keys = "welcome_channel_id",
            checks = {'id' : guild_id}
        )

        channel = self.bot.get_channel(
            result["welcome_channel_id"]
        )

        await channel.send(f'{member.mention} has joined the server!')

def setup(bot):
    bot.add_cog(WelcomeActions(bot))