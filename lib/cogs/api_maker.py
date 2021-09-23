import requests
import asyncio
from discord.ext.commands import command, Cog
from discord import Embed

class API(Cog):
    def __init__(self, bot):
        pass

    # @command(name="mdl")
    # async def package(self, ctx, arg, arg2):
    #     if arg == "find":
    #         modl_url = "https://pypi.org/search/?q=" + arg2
    #         modl = requests.get(modl_url)
    #         f = modl.json()
    #         if not "error" in f:
    #             name = f["package"]
    #             version = f["version"][0]["version"]
    #             embed = Embed(title=f"{arg2}", color=0xd70751, description = f"Python Modules")
    #             embed.add_field(name="Version:", value=f"{version}")
    #             message = await ctx.send(embed=embed)
    #             await message.add_reaction("🗑")

    #             def check(reaction, user):
    #                 return user == ctx.message.author and str(reaction.emoji) == '🗑'

    #             try:
    #                 await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
    #             except asyncio.TimeoutError:
    #                 print("Ha pasado el tiempo de espera.")
    #             else:
    #                 await message.delete()
    #         else:
    #             srch_url = "https://pypi.org/search/?q=" + arg2
    #             srch = requests.get(srch_url)
    #             j = srch.json()
    #             other = j["result"]["other"]
    #             one = other[0]["name"]
    #             embed = Embed(title="Modulo no encontrado", color=0xff0000, description="Quisiste decir:")
    #             embed.add_field(name=f"{one}", value="Desde pypi.org")
    #             await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(API(bot))