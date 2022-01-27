from discord.ext.commands import command, Cog
from discord.ext.commands.errors import BadArgument, MissingRequiredArgument
from discord import Embed
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption, component, interaction

class Publisher(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Send embed with a info the specific guild

    @command(name="info", aliases=['i'])
    async def info(self, ctx):
        embed=Embed(title="Flangsbot", url="http://flangscom.herokuapp.com", color=0xa244d5)
        embed.set_author(name="Flangrys", url="https://twitter.com/flangrys_", icon_url="./data/images/thumbnail.gif")
        embed.set_footer(text="Encontra mas informacion en nuestro sitio oficial.")

        await ctx.send(
            embed=embed,
            components=[
                Select(
                    placeholder = "Opciones",
                    max_values = '3',
                    options = [
                        SelectOption(label = "Dashboard", value = "https://flangscom.herokuapp.com"),
                        SelectOption(label = "Twitter", value = "https://twitter.com/flangrys_"),
                        SelectOption(label = "GitHub", value = "https://github.com/flangrys/flangsbot")
                    ]
                )
            ]
            
        )
        while True:
            interaction = await self.bot.wait_for("select_option")
            await interaction.respond(
                content = f"{','.join(map(lambda x: x.label, interaction.selected_options))} seleccionado",
            )


def setup(bot):
    bot.add_cog(Publisher(bot))