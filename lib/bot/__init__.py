import platform
print(platform.python_version())

from datetime import datetime

from discord import Embed, File
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

from ..db import db

PREFIX = "$"
OWNER_IDS = ['546542419399802884']


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS)
    
    def run(self, VERSION):
        self.VERSION = VERSION

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()
        
        print("Loading Flangsbot")
        print("----------")
        super().run(self.TOKEN, reconnect=True)

    async def rules_reminder(self):
        channel = self.get_channel(811778663996456990)
        await channel.send("Remember to adhere to the rules!")

    async def on_connect(self):
        print("Connected")
        print("----------")

    async def on_disconnect(self):
        print("Disconnected")
        print("----------")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went worng.")

        raise

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
            self.guild = self.get_guild(651231834356711427)
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()


            print("Flangscom is ready")
            print("----------")

            #channel = self.get_channel(811778663996456990)
            #embed = Embed(title="Running bot", description="Flangsbot is now online", color=0xe17856, timestamp=datetime.utcnow())
            #fields = [("Name", "Value", True), ("another field", "this field is next to the other one.", True), ("A non-inline field", "this field will appear on it's own row", False)]
            #for name, value, inline in fields:
            #    embed.add_field(name=name, value=value, inline=inline)
            #embed.set_author(name="Flan", icon_url=self.guild.icon_url)
            #embed.set_footer(text="This is a footer!")
            #await channel.send(embed=embed)
            #await channel.send(fiel=File("./data/images/profile.png"))

        else:
            print("Bot Reconnected")

    async def on_message(self, message):
        pass


Bot = Bot()