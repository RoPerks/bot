import discord
from discord.ext import commands
from cogs.info import EmbedHelpCommand
import darealmodule

class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.BadArgument):
            embed=discord.Embed(title="You did not give valid permiters for that command.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}help {ctx.command}` for help.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.NotOwner):
            embed=discord.Embed(title="You don't have permissions to run this command.", description=f'<:warningerrors:713782413381075536> `{ctx.prefix}{ctx.command}` has been restricted to owner usage only.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title="You lack the permissions to run that command.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}help {ctx.command}` for further support.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="You are missing required arguments for that command.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}help {ctx.command}` for help.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CommandOnCooldown):
            embed=discord.Embed(title=f"Cooldown is active.", description=f'<:warningerrors:713782413381075536> The command `{ctx.prefix}{ctx.command}` can only be called once every 30 seconds.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.BotMissingPermissions):
            error = " ".join(str(error).split(" ")[2:4])
            embed=discord.Embed(title=f"Invalid Permissions.", description=f'<:warningerrors:713782413381075536> `{self.bot.user.name}` requires `{error}` to run `{ctx.prefix}{ctx.command}`.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.send(embed=embed)
            return
        if isinstance(error, commands.CheckFailure):
            return
        
        await self.bot.std_error.send(f'```python\n{error}\n```')
        await self.bot.std_error.send(f'```json\n{ctx.__dict__}\n```')



async def setup(bot):
    await bot.add_cog(Errors(bot))
