import platform
import os
import discord
import logging as log

from asyncio.tasks import sleep
from glob import glob

#from ..db import model
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from cogwatch import watch
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot as BotBase
from discord.ext.commands.errors import BadArgument, CommandNotFound
from discord.ext.commands.context import Context
from discord.errors import Forbidden, HTTPException
from discord_components import DiscordComponents

FORMAT = "[%(asctime)s]:[%(levelname)s] $%(name)s @: %(message)s"
log.basicConfig(format=FORMAT, level=log.DEBUG, filename="bot.log")

log.debug(f'Python Enviroment Version:{platform.python_version()}')

PREFIX = "$"
OWNER_IDS = [546542419399802884]
COGS = [path.split("\\")[-1][:-3] for path in glob("./Flangsbot/src/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

intents = discord.Intents.default()
intents.members = True


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

    def ready_up(self, cog) -> None:
        """Sets the cog to ready"""
        setattr(self, cog, True)
        log.info(f'COG LOADER >>> [{cog}] -> READY')
    
    def all_ready(self) -> bool:
        """Return True if all cogs are ready"""
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        
        super().__init__(command_prefix=PREFIX, owner_ids=OWNER_IDS, help_command=CustomHelpCommand(), intents=intents)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"Flangsbot.src.cogs.{cog}")
            log.warn(f'COG LOADER >>> [{cog}] -> LOADED')

        log.info(' !> SETUP COMPLETE!')


    def run(self, VERSION):
        self.VERSION = VERSION
        self.TOKEN = os.getenv('FLANGSBOT_KEY')

        log.info(f'Flangsbot Development Version: {self.VERSION}')
        log.warn(f'!> RUNNING SETUP')

        self.setup()

        log.warn('!> LOADING FLANGSBOT')

        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.command != None and ctx.guild != None:
            if self.ready:
                await self.invoke(ctx)
            else:
                await ctx.send("!- I'm not ready to recive commands. Please wait a few seconds.")            

    async def rules_reminder(self):
        await self.stdout.send("!- ¡Remember to adhere to the rules!")

    async def on_connect(self):
        log.critical('>>> CONNECTED')

    async def on_disconnect(self):
        log.critical('>>> DISCONNECTED')
        log.warn('!> RESTARTING')

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            # Errno: WORNG_COMMAND
            await args[0].send(f"!~ Se produjo un error inesperado 0x000100.\n !~ {err}")
        # Errono: UNKNOW_COMMAND
        await self.stdout.send(f"!~ Se produjo un error inesperado 0x000404.\n !~ {err}")
        raise
    
    #TODO: If going to work with new cog system, delete this lines bellow because isn't needed
    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            await ctx.send(f"{exc}")

        elif isinstance(exc, HTTPException):
            await ctx.send(f"{ctx.author.mention} ¡No se pudo enviar el mensaje!")

        elif isinstance(exc, Forbidden):
            await ctx.send(f"{ctx.author.mention} ¡No tengo permisos para hacer esto!")

        else:
            embd1 = Embed(
                title="***¡Boo boo!***",
                url="https://flangscom.herokuapp.com",
                description="¡No se ha podido detectar el problema!",
                color=0xca5624
            ).add_field(
                name="Administrador:", value='<@!546542419399802884>'
            )
            
            await ctx.send(embed=embd1)
            await ctx.send(f"'{exc}'")

    @watch(path='Flangsbot/src/cogs')
    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.cogs_ready = Ready()
            self.guild = self.get_guild(651231834356711427) # !Deprecated
            self.stdout = self.get_channel(845523083700076544) # !Deprecated

            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=0, minute=5, second=0))
            self.scheduler.start()
            
            DiscordComponents(Bot)

            log.info(f'>>> FLANGSBOT READY')

            embd2=Embed(
                title='***Flangscom Environment***',
                url="https://discord.com/channels/910550055226863656/911320937712975932", 
                description="Para reportar errores puedes hacerlo en el link del titulo del embed.", 
                color=0xca5624
            )
            embd2.set_author(name="Flangsbot", url="https://flangscom.herokuapp.com", icon_url=self.guild.icon_url)
            embd2.set_footer(text="by Flangrys#7673 | by Flangscom™", icon_url=self.guild.icon_url)
            embd2.set_thumbnail(url=self.guild.icon_url)

            await self.stdout.send(embed=embd2)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

        else:
            log.critical(f'>>> RECONNECTED')

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


flan = Bot()