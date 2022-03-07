from Flangsbot.src.db.backend.base import Database

import logging

logging.getLogger(__name__)

class GuildMDB:
    def __init__(self, database, guild_id):
        self.database = database
        self.guild_id = guild_id

    async def create_guild(self):
        logging.warn(f'Creating guild table as {self.guild_id}')
        self.database.create_table(
            table_name = f"Guild_{self.guild_id}",
            columns = {
                "log_channel_id": "INTEGER",
                "welcome_channel_id": "INTEGER",
                "tickets_channel_id": "INTEGER",
            },
            not_exists = True
        )

    async def delete_teble(self):
        logging.warn(f'Deleting guild table as {self.guild_id}')
        self.database.delete(
            table_name = f"Guild_{self.guild_id}"
        )

    async def select(self, keys):
        return self.database.select(
            table_name = f"Guild_{self.guild_id}",
            key = [keys]
        )

    async def select_where(self, keys, checks):
        return self.database.select(
            table_name = f"Guild_{self.guild_id}",
            key = [keys],
            checks = checks
        )