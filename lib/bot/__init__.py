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

    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r" encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running Bot ....")
        print("----------")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect():
        print('Flangsbot is online.')
        print('----------')

    async def on_disconnect():
        print("Flangsbot is offline")
        print("----------")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(651231834356711427)
            print("Flangsbot Ready")
            print('Logged in as ->', self.client.user)
            print('ID', self.client.user.id)
            print('----------')
        else:
            print("Flngsbot reconnected")
            print("----------")

    async def on_message(sewlf, message):
        pass


bot = Bot()
