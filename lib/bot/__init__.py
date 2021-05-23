from asyncio.tasks import sleep
from datetime import datetime
from glob import glob
from os import path

from discord.ext.commands import CommandNotFound
from discord.ext.commands import Bot as BotBase
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Embed, File

from ..db import db

import platform
print(platform.python_version())


PREFIX = "$"
OWNER_IDS = ['546542419399802884']
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

class Ready(object):
    def __init__(self):
       for cog in COGS:
           setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" {cog} cog ready") 
    
    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} Cog loaded!")

        print("Setup complete")

    def run(self, VERSION):
        self.VERSION = VERSION

        print("Running Setup ....")
        self.setup()

        with open("./lib/bot/token.txt", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Loading Flangsbot")
        print("----------")
        super().run(self.TOKEN, reconnect=True)

    async def rules_reminder(self):
        await self.stdout.send("Remember to adhere to the rules!")

    async def on_connect(self):
        print("Connected")
        print("----------")

    async def on_disconnect(self):
        print("Disconnected")
        print("----------")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went worng.")
            
        await self.stdout.send("Se produjo un error inesperado 0x000404.")
        #raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.cogs_ready = Ready()
            self.guild = self.get_guild(651231834356711427)
            self.stdout = self.get_channel(845523083700076544)
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()

            print("Flangscom is ready")
            print("----------")

            await self.stdout.send("Flangscom is ready")

            #embed = Embed(title="Running bot", description="Flangsbot is now online", color=0xe17856, timestamp=datetime.utcnow())
            #fields = [("Name", "Value", True), ("another field", "this field is next to the other one.",True), ("A non-inline field", "this field will appear on it's own row", False)]
            #for name, value, inline in fields:
            #    embed.add_field(name=name, value=value, inline=inline)
            #embed.set_author(name="Flan", icon_url=self.guild.icon_url)
            #embed.set_footer(text="This is a footer!")
            #await self.stdout.send(embed=embed)
            #await self.stdout.send(file=File("./data/images/profile.png"))

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

        else:
            print("Bot Reconnected")

    async def on_message(self, message):
        pass


Bot = Bot()