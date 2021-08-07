from discord.ext.commands import command, Cog
from discord.ext.commands.core import has_permissions
from discord.ext.commands.errors import MissingPermissions, MissingRequiredArgument
from discord import Embed


class Manager(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="clear", aliases=["cls", "clsc"])
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, ammount:int):
        if (ammount <= 9):
            await ctx.send(f"Solo puedes borrar 30 mensajes de golpe")
        elif (ammount == 10):
            await ctx.channel.purge(limit=ammount)
        else:
            await ctx.channel.purge(limit=ammount)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention} Especifica la cantidad de mensajes.")

        if isinstance(error, MissingPermissions):
            await ctx.send(f"{ctx.author.mention} No tienes los permisos necesarios.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.reday_up("manager")

def setup(bot):
    bot.add_cog(Manager(bot))