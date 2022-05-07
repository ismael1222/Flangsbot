import os
import platform
import logging as log

from asyncio.tasks import sleep

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from discord import Embed, Intents
from discord.ext.commands.context import Context
from discord.ext.commands import Bot as BotBase
from discord.errors import Forbidden, HTTPException

from .config import FMT, PREFIX, OWNER_IDS, COGS, IGNORE_EXCEPTIONS
from .helpcommand import Help
from .preloader import Preload
from .utils import Configuration

log.basicConfig(
    level=log.DEBUG,
    format=FMT
)

log.debug(f'Python Enviroment Version:{platform.python_version()}')

intents = Intents.default()
intents.members = True

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready: bool = False
        self.scheduler: AsyncIOScheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix = PREFIX, 
            owner_ids = OWNER_IDS, 
            help_command = Help, 
            intents = intents
        )

    def _setup(self):
        for cog in COGS:
            self.load_extension(f"Flangsbot.src.cogs.{cog}")
            log.warn(f'COG LOADER >>> [{cog}] -> LOADED')

        log.info(' !> SETUP COMPLETE!')

    def run(self, VERSION):
        self.VERSION = VERSION
        self.TOKEN = os.getenv('FLANGSBOT_KEY')

        log.info(f'Flangsbot Development Version: {self.VERSION}')
        log.warn(f'!> RUNNING SETUP')

        self._setup()

        log.warn('!> LOADING FLANGSBOT')

        super().run(self.TOKEN, reconnect=True)

    def stop(self):
        log.critical('>>> STOPPING!')
        self.close()

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.command != None and ctx.guild != None:
            if self.ready:
                await self.invoke(ctx)
            else:
                #TODO: Fix context void
                await ctx.send("!- I'm not ready to recive commands. Please wait a few seconds.")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.preload = Preload()
            self.ch = self.get_channel(845523083700076544)
            self.guild = self.get_guild(651231834356711427) # !Deprecated

            log.info(f'>>> FLANGSBOT READY')

            embd2=Embed(
                title='***Flangscom Environment***',
                url="https://discord.com/channels/910550055226863656/911320937712975932", 
                description="", 
                color=0xca5624
            )
            embd2.set_author(name="Flangsbot", url="https://flangscom.herokuapp.com", icon_url=self.guild.icon_url)
            embd2.set_footer(text="Developed by Flangscom™ | Flangrys#7673", icon_url=self.guild.icon_url)

            await self.ch.send(embed=embd2)

            while not self.preload.all_ready():
                await sleep(0.5)

        else:
            log.critical(f'>>> RECONNECTED')

    async def on_connect(self):
        log.critical('>>> CONNECTED')

    async def on_disconnect(self):
        log.critical('>>> DISCONNECTED')
        log.warn('!> RESTARTING')

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

    #TODO: Refctor this to be more generic
    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send(f"Se produjo un error en el comando: {err} \n [0x000100]")
        await self.get_channel(845523083700076544).send(f"Se produjo un error inesperado: {err} \n [0x000404]")
        raise
    
    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            await ctx.send(f"{exc}")

        elif isinstance(exc, HTTPException):
            await ctx.send(f"{ctx.author.mention} ¡No se pudo enviar el mensaje!")

        elif isinstance(exc, Forbidden):
            await ctx.send(f"{ctx.author.mention} ¡No tengo permisos para hacer esto!")

        else: #NOTE: This is the default error handler, but can overlap with the cogs command error.
            embd1 = Embed(
                title="***¡Boo boo!***",
                url="https://flangscom.herokuapp.com",
                description="Que cagada hiciste, no se que pasó pero no se que pasó.",
                color=0xca5624
            )
            embd1.add_field(
                name=f'Exception Raised', value=f'{exc}', inline=True
            )
            
            await ctx.send(embed=embd1)

flan = Bot()