from discord.ext.commands import command, Cog
from discord.member import Member
from discord.embeds import Embed

from random import choice, random
from typing import Optional


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="ping")
    async def pong(self, ctx):
        await ctx.send(f"Pong!")

    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hola', 'Hya', 'Hi', 'Helouda', 'Ñe', 'ola', 'ke ase vo', 'ola guap@', 'Buenas'))} {ctx.author.mention}!")

    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "nada"):
        await ctx.send(f"{ctx.author.display_name} cacheteo a {member.mention} por {reason}❗")

    @command(name="echo", aliases=['say'])
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @command(name="lat", aliases=['lms', 'ms'])
    async def latency(self, ctx):
        await ctx.send(f"⏳ = {round(self.latency * 1000)}ms")

    @command(name="eightball", aliases=['8ball', 'bolaocho','b8'])
    async def eightball(self, ctx, *, question, error):
        responses = ["Es seguro", "Es decididamente así", "Sin duda", "Puedes confiar en ello", "Tal como lo veo, si", "Lo mas probable", "Si", "Los signos apuntan al si", "Respuesta confusa, intentalo de nuevo", "Vuelve a preguntar mas tarde",
                     "Mejor no te lo digo ahora", "No puedo predecirlo en este momento", "Concentrate y vuelve a preguntar", "Mi respuesta es un no", "Mis fuentes dicen que no", "No cuentes con ello", "Las perspectivas no son tan buenas", "Muy dudoso"]
        embed=Embed(title='**8Ball**', color=0xfff0ff)
        embed.add_field(name='***Tu pregunta***', value={question}, inline=True)
        embed.add_field(name='***Mi respuesta***', value={random.choice(responses)}, inline=True)
        embed.set_footer(text='Espero que esta respuesta alla sido de tu agrado 😀')
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
