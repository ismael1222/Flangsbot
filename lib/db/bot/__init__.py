from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = "$"
OWNER_IDS = [546542419399802884]

class Bot(BotBase):
    def __ini__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)


    def run():
        pass

    async def on_connect():
        print('Flangsbot is online.')
        print('Logged in as ->', self.client.user)
        print('ID', self.client.user.id)
        print('----------')

    async def on_disconnect():
        print("Flangsbot is offline")
        print("----------")