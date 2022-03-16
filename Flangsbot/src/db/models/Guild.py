from Flangsbot.src.db.backend.base import Database
from Flangsbot.src.db.manager import DataBaseManager

class UnknownGuild(Exception): ... #NOTE: Raise this exception when the guild is not in the database or was wrong defined.

class GuildTable:
    def __init__(self, database: Database, guild_id):
        self.database = DataBaseManager.db_type(database)
        self.guild_id = guild_id

        result = self.database.execute(
            sql_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='Guild_{}'".format(self.guild_id)
        )
        if result == 0:
            raise UnknownGuild(f"The guild {self.guild_id} is not in the database.")

    async def create_guild(self):
        await self.database.create_table(
            table_name = f"Guild_{self.guild_id}",
            columns = {
                "log_channel_id": "INTEGER",
                "welcome_channel_id": "INTEGER",
                "tickets_channel_id": "INTEGER",
                "tickets_category_id": "INTEGER",
                "lang": "INTEGER",
            },
            not_exists = True
        )

    async def delete_teble(self):
        await self.database.delete(
            table_name = f"Guild_{self.guild_id}"
        )

    async def select(self, keys):
        return await self.database.select(
            table_name = f"Guild_{self.guild_id}",
            keys = [keys]
        )

    async def select_where(self, keys, checks):
        return await self.database.select(
            table_name = f"Guild_{self.guild_id}",
            key = [keys],
            checks = checks
        )