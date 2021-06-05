from discord.ext.commands import command, Cog
from discord.ext.commands.errors import MissingRequiredArgument
from discord import Embed

class Clear(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="clear", aliases=["cls", "clx"])
    async def clear(self, ctx, amount:int):
        if(amount >= 30):
            await ctx.send(f"✖ No puedes borrar mas de 30 mensajes a la vez. ❗")
        else:
            await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"❗❗❗{ctx.author.mention}❗❗❗ Especificame cuantos mensajes queres que borre.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("clear")

def setup(bot):
    bot.add_cog(Clear(bot))
