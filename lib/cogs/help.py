from discord.ext.commands import command, Cog
from discord.ext.commands.errors import BadArgument, MissingRequiredArgument
from discord_components import Button, Select, SelectOption

class Help(Cog):
    def __init__(self, bot):
        self.bot = bot

@command(name="help")
async def help(self, ctx):
    await ctx.send(
        ":flag_ar:"
    )

def setup(bot):
    bot.add_cog(Help(bot))
