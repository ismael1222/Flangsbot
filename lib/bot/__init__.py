import platform
import discord
import os

from asyncio.tasks import sleep
from datetime import datetime
from glob import glob

from ..db import db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from cogwatch import watch
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot as BotBase
from discord.ext.commands.errors import BadArgument, CommandNotFound, MissingPermissions, MissingRequiredArgument
from discord.ext.commands.context import Context
from discord.errors import Forbidden, HTTPException
from discord_components import DiscordComponents

print(f"[ENVIRONMENT] Python Enviroment >> {platform.python_version()}")


PREFIX = "$"
OWNER_IDS = ['546542419399802884']
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

intents = discord.Intents.default()
intents.members = True

"""Se establece el comportamiento del comando $help <args>"""

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        for cog in mapping:
            await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in mapping[cog]]}')

    async def send_cog_help(self, cog):
        await self.get_destination().send(f'{cog.quailified_name}: {[command.name for command in cog.get_commands()]}')
    
    async def send_group_help(self, group):
        await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')

    async def send_command_help(self, command):
        await self.get_destination().send(command.name)

class Ready(object):
    def __init__(self):
        
        for cog in COGS:
           setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"[INFORMATION] [{datetime.utcnow()}] >> ![{cog}] Cog Ready") 
    
    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, help_command=CustomHelpCommand(), intents=intents)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"[INFO] [{datetime.utcnow()}] >> !- [{cog}] COG LOADED")

        print(f"[INFO] [{datetime.utcnow()}] >> !- SETUP COMPLETE")

    def run(self, VERSION):
        self.VERSION = VERSION

        print(f"[ENVIROMENT] Version >> {self.VERSION}")
        print(f"[INFO] [{datetime.utcnow()}] >> !- RUNNING SETUP")

        self.setup()

        self.TOKEN = os.getenv('FLANGSBOT_KEY')

        print(f"[INFO] [{datetime.utcnow()}] >> !- Loading Flangsbot")

        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)
            else:
                await ctx.send("!- I'm not ready to recive commands. Please wait a few seconds.")            

    async def rules_reminder(self):
        await self.stdout.send("!- ¡Remember to adhere to the rules!")

    async def on_connect(self):
        print(f"[INFO] [{datetime.utcnow()}] >> !~ CONNECTED")

    async def on_disconnect(self):
        print(f"[INFO] [{datetime.utcnow()}] >> !~ DISCONNECTED")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            # Errno: WCOMMAND
            await args[0].send(f"!~ Se produjo un error inesperado 0x000100.\n !~ {err}")
            # 
        await self.stdout.send(f"!~ Se produjo un error inesperado 0x000404. \n !~ {err}")
        raise
    
    # Si se va trabajan los cogs con errores independientes, eliminar esto de abajo porque no es enecesario.
    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            await ctx.send(f"{exc}")

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention} Faltan uno o mas argumentos necesarios requeridos")

        elif isinstance(exc, HTTPException):
            await ctx.send(f"{ctx.author.mention} ¡No se pudo enviar el mensaje!")

        elif isinstance(exc, Forbidden):
            await ctx.send(f"{ctx.author.mention} ¡No tengo permisos para hacer esto!")

        elif isinstance(exc, MissingPermissions):
            await ctx.send(f"{ctx.author.mention} ¡No tienes permisos para hacer esto!")

        else:
            raise exc.original

    @watch(path='lib/cogs')
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.cogs_ready = Ready()
            self.guild = self.get_guild(651231834356711427) # !Deprecated
            self.stdout = self.get_channel(845523083700076544) # !Deprecated
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()
            DiscordComponents(Bot)

            print(f"[INFO] [{datetime.utcnow()}] >> !- Flangsbot is ready!")

            embed=Embed(title="🤖 Estoy Activo ❗", url="https://discord.com/channels/651231834356711427/850494763160567858", description="Si encuentras algún tipo de error o bug, reportalo en el canal de ", color=0xca5624, timestamp=datetime.utcnow())
            embed.set_author(name="Flangsbot", url="https://flangscom.herokuapp.com", icon_url=self.guild.icon_url)
            embed.set_footer(text="by Flangscom team")
            embed.set_thumbnail(url=self.guild.icon_url)
            await self.stdout.send(embed=embed)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

        else:
            print(f"[WARN] [{datetime.utcnow()}] >> !- RECONNECTED")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


Bot = Bot()