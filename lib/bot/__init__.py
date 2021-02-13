from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = "$"
OWNER_IDS = [546542419399802884]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running setup ....")
        print("----------")
        super().run(self.TOKEN, reconnect=True)

	async def on_connect(self):
		print("Flangsbot is online")
        print("----------")

    async def on_disconnect(self):
        print("Flangsbot is offline")
        print("----------")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(651231834356711427)
            print("Flangsbot Ready")
            print('----------')
        else:
            print("Flngsbot reconnected")
            print("----------")

    async def on_message(self, message):
        pass


bot = Bot()
