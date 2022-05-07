from discord.ext.commands import command, Cog
from discord.member import Member
from discord.message import Message

class AutoMod(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        ...

    @command(name = "ban")
    async def ban(self, ctx, user: Member, *, reason: str):
        ...

    @command(name = "unban")
    async def unban(self, ctx, user: Member):
        ...

    @command(name = "mute")
    async def mute(self, ctx, user: Member, *, reason: str):
        ...

    @command(name = "unmute")
    async def unmute(self, ctx, user: Member):
        ...

    @command(name = "kick")
    async def kick(self, ctx, user: Member, *, reason: str):
        ...

def setup(bot):
    bot.add_cog(AutoMod(bot))