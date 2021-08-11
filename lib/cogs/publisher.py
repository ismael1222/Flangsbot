from discord.ext.commands import command, Cog
from discord.ext.commands.errors import BadArgument, MissingRequiredArgument
from discord import Embed
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption, component, interaction

class Publisher(Cog):
    def __init__(self, bot):
        self.bot = bot

#-> Send Embed
@command(name="info", aliases=['i'])
async def info(self, ctx):
    embed=Embed(title="Flangsbot", url="http://flangscom.herokuapp.com", color=0xa244d5)
    embed.set_author(name="Flangrys", url="https://twitter.com/flangrys_", icon_url="./data/images/thumbnail.gif")
    embed.set_footer(text="Encontra mas informacion en nuestro sitio oficial.")

    await ctx.send(
        embed=embed,
            component = [
            Button(style=ButtonStyle.grey, label="Web Site", emoji="🌐"),
            Button(style=ButtonStyle.grey, label="Invite", disable=True)
        ]
    )
    while True:
        interaction = await self.bot.wait_for("button_click")
        await interaction.respond(content=f"{interaction.component.label} clickeado!")

def setup(bot):
    bot.add_cog(Publisher(bot))