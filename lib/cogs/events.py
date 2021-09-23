from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands.errors import BadArgument, MissingRequiredArgument

from discord.embeds import Embed

class Events(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        channel = self.bot.get_channel("742914614274162738")
        embd = Embed(title = f"**Welcome {member.mention} to Flangscom** ")
        await ctx.channel.send(embd)

def setup(bot):
    bot.add_cog(Events(bot))