import discord

from discord.ext.commands import command, Cog
from discord.ext.commands import has_guild_permissions, MissingPermissions, MissingRequiredArgument, MissingRole
from discord.ext.commands.errors import MemberNotFound
from discord.embeds import Embed

class Moderation(Cog):
    """
    Moderation Commands        
    """
    def __init__(self, bot):
        self.bot = bot

    @command(name="clear", aliases=["cls"])
    @has_guild_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = None):
        if (amount >= 10):
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'Se han eliminado {amount} mensajes', delete_after=3)
        else:
            await ctx.send(f"!Solo puedes borrar 10 mensajes a la vez")
            
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("!No tienes permisos para usar este comando.")
        elif isinstance(error, MissingRole):
            await ctx.send("!No tienes el rol necesario para usar este comando.")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("!Falta un argumento requerido.")

    @command(name="ban")
    @has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str):
        await member.ban(reason=reason)

        emb = Embed(title=f'~~Cagatse~~', description=f'{member.mention} ha sido baneado por {ctx.author.mention}', color=0xFFC500)
        emb.set_thumbnail(url=member.avatar_url)
        emb.add_field(name='Motivo', value=reason)
        emb.add_field(name='Fecha de emision', value=ctx.message.created_at, inline=True)
        emb.set_footer(text=f'Demogorgon | Developed by Flangrys#7673')
        
        await ctx.send(embed=emb)

    @ban.error
    async def ban_error(self, ctx, err):
        if isinstance(err, MissingRequiredArgument):
            await ctx.send("!Falta un argumento requerido.")
        if isinstance(err, MemberNotFound):
            await ctx.send("⛔ !No se ha encontrado el usuario.")
        if isinstance(err, MissingPermissions):
            await ctx.send("!No tienes permisos para usar este comando.")
        if isinstance(err, MissingRole):
            await ctx.send("!No tienes el rol necesario para usar este comando.")

    @command(name='report')
    @has_guild_permissions(ban_members=True)
    async def report(self, ctx, member: discord.Member, *, reason: str = None):

        emb = Embed(title=f'~~**Reporte**~~', description=f'{member.mention} ha sido reportado por {ctx.author.mention}', color=0xFFC500)
        emb.set_thumbnail(url=member.avatar_url)
        emb.add_field(name='Motivo', value=reason)
        emb.add_field(name='Fecha de emision', value=ctx.message.created_at, inline=True)
        emb.set_footer(text=f'Demogorgon | Developed by Flangrys#7673')

        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(Moderation(bot))