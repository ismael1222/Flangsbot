from discord.ext.commands import command, Cog
from discord.ext.commands.errors import BadArgument, MissingRequiredArgument
from discord import Embed

class Publisher(Cog):
    def __init__(self, bot):
        self.bot = bot

#-> Send Embed
@command(name="xembed")
async def xembed(self, ctx, error):
    #stdout_rules = self.get_channel(651232875198283788)
    embed=Embed(title="Official rules of Flangscom", url="http://flangscom.herokuapp.com/rules", color=0xa244d5)
    embed.set_author(name="Flangrys", url="https://twitter.com/flangrys_", icon_url="./data/images/thumbnail.gif")
    embed.add_field(name="", value="", inline=True)
    embed.add_field(name="Normas2", value="Valores2", inline=True)
    embed.set_footer(text="Encontra mas informacion en nuestro sitio oficial.")
    await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Publisher(bot))
