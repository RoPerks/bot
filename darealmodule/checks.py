from abc import abstractmethod
import discord
from discord.ext import commands, tasks
import darealmodule

class Checks:

    @staticmethod
    async def run_if_not_configured(ctx):
        if await ctx.bot.db_pool.fetchval('SELECT EXISTS (SELECT 1 FROM guild_dump WHERE guild_id=$1)', ctx.guild.id):
            embed=discord.Embed(title="Already configured.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}{ctx.command} delete` to delete values, then use `{ctx.prefix}setup` to reconfigure.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(ctx.cog, ctx))
            await ctx.send(embed=embed)
            raise commands.CheckFailure
        
        return True

    @staticmethod
    async def run_if_configured(ctx):
        if not await ctx.bot.db_pool.fetchval('SELECT EXISTS (SELECT 1 FROM guild_dump WHERE guild_id=$1)', ctx.guild.id):
            embed=discord.Embed(title="Guild not configured.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}help setup` for more help.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(ctx.cog, ctx))
            await ctx.send(embed=embed)
            raise commands.CheckFailure
        
        return True

    @staticmethod
    async def check_configuration_status(bot, guild):
        if await bot.db_pool.fetchval('SELECT EXISTS (SELECT 1 FROM guild_dump WHERE guild_id=$1)', guild.id):
            return True
        return False
