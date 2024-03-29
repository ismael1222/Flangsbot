from discord.ext.commands import command, Cog
from discord.ext.commands.errors import BadArgument, MissingRequiredArgument
from discord.member import Member
from discord.embeds import Embed

from aiohttp import request
from random import choice, random

class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot
#-> Ping pong
    @command(name="ping")
    async def pong(self, ctx):
        await ctx.send("Pong!")

#-> Slap
    @command(name="slap", aliases=["hit"])
    async def slap_member(self, ctx, member: Member, *, reason: str = 'nada en lo absoluto'):
        await ctx.send(f"{ctx.author.display_name} cacheteo a {member.mention} por {reason}❗")

    @slap_member.error
    async def slap_member_error(self, ctx, error, exc):
        if isinstance(exc, BadArgument):
            await exc.send("¡Ese comando no existe!")

#-> Echo
    @command(name="echo", aliases=['say'])
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)
        
#-> Latency
    @command(name="lat", aliases=['lms', 'ms'])
    async def latency(self, ctx):
        await ctx.send(f"⏳ = {round(self.latency * 1000)}ms")

#-> Eightball
    @command(name="eightball", aliases=['8ball', 'bolaocho','b8'])
    async def eightball(self, ctx, error, *, question):
        responses = ["Es seguro", "Es decididamente así", "Sin duda", "Puedes confiar en ello", "Tal como lo veo, si", "Lo mas probable", "Si", "Los signos apuntan al si", "Respuesta confusa, intentalo de nuevo", "Vuelve a preguntar mas tarde",
                     "Mejor no te lo digo ahora", "No puedo predecirlo en este momento", "Concentrate y vuelve a preguntar", "Mi respuesta es un no", "Mis fuentes dicen que no", "No cuentes con ello", "Las perspectivas no son tan buenas", "Muy dudoso"]
        embed=Embed(title='**8Ball**', color=0xfff0ff)
        embed.add_field(name='***Tu pregunta***', value={question}, inline=True)
        embed.add_field(name='***Mi respuesta***', value={random.choice(responses)}, inline=True)
        embed.set_footer(text='Espero que esta respuesta alla sido de tu agrado 😀')
        await ctx.send(embed=embed)

    @eightball.error
    async def eightball_error(self, ctx, exc, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("!- Se requiere de un ARGUMENTO valido")

    @command(name="fact")
    async def objet_fact(self, ctx, object: str):
        URL = "https://some-random-api.ml/meme"

        async with request("GET", URL, headers={}) as responses:
            if responses.status == 200:
                data = await responses.json()

                embed=Embed(title="💡 Facts ", url="https://some-random-api.ml", color=0x228acf)
                embed.set_thumbnail(url=data["image"])
                embed.add_field(name="***Respuesta***", value=f'{data["caption"]}', inline=True)
                embed.set_footer(text="Nobody!")
                await ctx.send(embed=embed)

            else:
                await ctx.send("API returned a {responses.status} status.")

    @command(name="flan")
    async def flan(self, ctx):
        flanes = ["http://images7.memedroid.com/images/UPLOADED142/561f3debf00d9.jpeg", "https://cdn.memegenerator.es/imagenes/memes/full/29/73/29733520.jpg"]
        embed=Embed(title="¿Te refieres a esto?", color=0x228acf)            
        embed.set_thumbnail(url=choice(flanes))
        embed.set_footer(text="Creador, te han mencionado.")
        await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(Misc(bot))
