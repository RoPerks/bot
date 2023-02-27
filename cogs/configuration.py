import discord
from discord.ext import commands
import darealmodule


class Configuration(commands.Cog):
    """Allows guild owners to configure RoPerks given guilds."""

    def __init__(self, bot):
        self.bot = bot
        self.icon = '<:Games:718138175792480286>'
        self.thumbnail = 'https://cdn.discordapp.com/attachments/801951909455724566/870358119799222423/433845.png'


    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.check(darealmodule.Checks.run_if_not_configured)
    @commands.hybrid_command(name="setup", help='Links RoPerks to your guild.')
    async def setup_command(self, ctx):

        """
        Adds the given discord server to our databases, allowing developers to use the API for the given discord server.
        
        __Extra__
        We currently only support `RoWifi` & `RoVer` as verification systems.
        We require a verification system in order to assosiate users discord ids with their roblox ids. 
        This list is expanding fast, however, these are the only 2 options for now.
        """

        def reaction_check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ('<:rcross:711530086251364373>', '<:check:711530148196909126>')
        
        def reaction_check_numeric(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactions
            

        await ctx.message.add_reaction('<a:loading:716280480579715103>')
        
        rowifi = ctx.guild.get_member(508968886998269962)
        rover = ctx.guild.get_member(298796807323123712)
        bloxlink = ctx.guild.get_member(426537812993638400)
        bots_cluster = list(filter(None, [rowifi, rover, bloxlink]))
        bots_cluster_len = len(bots_cluster)
        confirmed_verification_sys = ''
        reactions = ['<:numone:878698879963525260>', '<:numtwo:878698938130104350>', '<:numthree:878698975694323712>']

        if not bots_cluster:
            await ctx.message.clear_reactions()
            embed=discord.Embed(title="No verification systems found.", description=f'<:warningerrors:713782413381075536> Please check that you have either `RoWifi`, `RoVer` or `BloxLink` is in your server, use `{ctx.prefix}help {ctx.command}` for more information.', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await ctx.send(embed=embed)
            return
        
        if bots_cluster_len == 1:
            embed=discord.Embed(description=f'Please confirm that you would like to use `{bots_cluster[0].name}` as the verification system that `{self.bot.user.name}` uses to assosiate discord accounts with roblox accounts.\n[<:check:711530148196909126>] - Confirm\n[<:rcross:711530086251364373>] - Decline', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text='This prompt will automatically end in 120 seconds')
            await ctx.message.clear_reactions()
            message = await ctx.send(embed=embed)

            await message.add_reaction('<:check:711530148196909126>')
            await message.add_reaction('<:rcross:711530086251364373>')
            
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=reaction_check, timeout=120)
            except:
                await message.clear_reactions()
                embed=discord.Embed(title="Prompt timed out.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}{ctx.command}` to restart this prompt.', color=0x2f3136)
                embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
                await message.edit(embed=embed)
                return

            reacted_emoji = str(reaction.emoji)
            await message.clear_reactions()

            if reacted_emoji == '<:rcross:711530086251364373>':
                embed=discord.Embed(title="Prompt Cancelled.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}{ctx.command}` to restart this prompt.', color=0x2f3136)
                embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
                await message.edit(embed=embed)
                return
            
            confirmed_verification_sys = bots_cluster[0].name
            
        elif bots_cluster_len != 1:
            index = 0
            string = ""
            for index in range(bots_cluster_len):
                string += f"\n[{reactions[index]}] - {bots_cluster[index].name}"
            embed=discord.Embed(description=f'Please select the verification system you would like `{self.bot.user.name}` to use to assosiate discord accounts with roblox accounts.{string}', color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text='This prompt will automatically end in 120 seconds')
            await ctx.message.clear_reactions()
            message = await ctx.send(embed=embed)

            for index in range(bots_cluster_len):
                await message.add_reaction(reactions[index])
            
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=reaction_check_numeric, timeout=120)
            except:
                await message.clear_reactions()
                embed=discord.Embed(title="Prompt timed out.", description=f'<:warningerrors:713782413381075536> Use `{ctx.prefix}{ctx.command}` to restart this prompt.', color=0x2f3136)
                embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
                await message.edit(embed=embed)
                return

            reacted_emoji = str(reaction.emoji)
            await message.clear_reactions()

            if reacted_emoji == '<:numone:878698879963525260>':
                await ctx.send(bots_cluster[0].name)
                confirmed_verification_sys = bots_cluster[0].name
            
            elif reacted_emoji == '<:numtwo:878698938130104350>':
                await ctx.send(bots_cluster[1].name)
                confirmed_verification_sys = bots_cluster[1].name
                
            elif reacted_emoji == '<:numthree:878698975694323712>':
                await ctx.send(bots_cluster[2].name)
                confirmed_verification_sys = bots_cluster[2].name
                
        confirmed_verification_sys = confirmed_verification_sys.lower()
        token = await darealmodule.Helping.generate_api_key(self)
        
        await self.bot.db_pool.execute(f"INSERT INTO guild_dump VALUES ($1, $2, $3)", ctx.guild.id, confirmed_verification_sys, token)

        embed.description = f"<:check:711530148196909126> Successfully set `{confirmed_verification_sys}` as the verification system for `{ctx.bot.user.name}`. Use `{ctx.prefix}key` to view your **API-KEY**.\n\n<:Join:718154643095683142>*Can't figure it out?: [__click here for our support server__](https://discord.gg/nG2ZUjPuF9)*"
        embed.color = 0x2f3136
        await message.edit(embed=embed)
        
        premium_user_ids = [user.id for user in ctx.guild.premium_subscribers]

        data = await self.bot.db_pool.fetch('SELECT * FROM user_data WHERE guild_id=$1', ctx.guild.id)
        logged_user_ids = [int(user['discord_id']) for user in data]

        need_to_be_removed = list(set(logged_user_ids) - set(premium_user_ids))
        need_to_be_added = list(set(premium_user_ids) - set(logged_user_ids))
        for user in need_to_be_removed:
            if await self.bot.db_pool.fetchval('SELECT EXISTS (SELECT 1 FROM user_data WHERE guild_id=$1 AND discord_id=$2)', ctx.guild.id, user):
                await self.bot.db_pool.execute(f"DELETE FROM user_data WHERE guild_id=$1 AND discord_id=$2", ctx.guild.id, user)
        for user in need_to_be_added:
            if not await self.bot.db_pool.fetchval('SELECT EXISTS (SELECT 1 FROM user_data WHERE guild_id=$1 AND discord_id=$2)', ctx.guild.id, user):
                roblox_id = await darealmodule.Helping.get_discord_roblox(self, ctx.guild.id, user)
                if roblox_id:
                    await self.bot.db_pool.execute(f"INSERT INTO user_data VALUES ($1, $2, $3)", ctx.guild.id, user, roblox_id)
                        
    @commands.has_permissions(manage_guild=True)
    @commands.check(darealmodule.Checks.run_if_configured)
    @commands.hybrid_command(name="delete", help='Removes the given discord server from our databases.')
    async def delete_command(self, ctx):

        """
        Removes the given discord server from our databases.
        """
        
        await self.bot.db_pool.execute(f"DELETE FROM guild_dump WHERE guild_id=$1", ctx.guild.id)
        await self.bot.db_pool.execute(f"DELETE FROM user_data WHERE guild_id=$1", ctx.guild.id)
 
        embed=discord.Embed()
        embed.description = f'<:check:711530148196909126> Successfully removed all data assosiated with this server from `{self.bot.user.name}`.'
        embed.color = 0x2f3136
        await ctx.send(embed=embed)
 
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.check(darealmodule.Checks.run_if_configured)
    @commands.hybrid_command(name="key", help='Gets or Regenerates the guilds api key.')
    async def key_command(self, ctx):

        """
        Adds the given discord server to our databases, allowing developers to use the API for the given discord server.
        """

        def reaction_check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ('<:repeats:751037833774366780>', '<:check:711530148196909126>')

        await ctx.message.add_reaction('<a:loading:716280480579715103>')

        token = await darealmodule.Helping.get_api_key(self, ctx)

        embed=discord.Embed(description=f"[<:check:711530148196909126>] - I've copied my key\n[<:repeats:751037833774366780>] - Regenerate Key\n\nUse `{ctx.prefix}docs` for endpoints & API usage.\n\n**DO NOT SHARE - REGENERATE IF KEY LEAKED**\nClick to reveal > ||{token}||", color=0x2f3136)
        embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text='This message will automatically delete in 60 seconds')
        await ctx.message.clear_reactions()
        message = await ctx.send(embed=embed)
            
        await message.add_reaction('<:check:711530148196909126>')
        await message.add_reaction('<:repeats:751037833774366780>')
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=reaction_check, timeout=60)
        except:
            await message.delete()
            return

        reacted_emoji = str(reaction.emoji)

        if reacted_emoji == '<:check:711530148196909126>':
            await message.delete()
            return
        
        elif reacted_emoji == '<:repeats:751037833774366780>':
            await message.clear_reactions()
            await message.add_reaction('<a:loading:716280480579715103>')
            
            token = await darealmodule.Helping.generate_api_key(self)
            await self.bot.db_pool.execute(f"UPDATE guild_dump SET api_key=$1 WHERE guild_id=$2", token, ctx.guild.id)
            
            embed.description = f'<:check:711530148196909126> Successfully Generated new API-KEY. Use `{ctx.prefix}{ctx.command}` to view the new API-KEY'
            embed.color = 0x2f3136
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
            await message.clear_reactions()
            await message.edit(embed=embed)
           
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.check(darealmodule.Checks.run_if_configured)
    @commands.hybrid_command(name="refresh", help='Updates the roblox account bound to your discord.')
    async def refresh_command(self, ctx):
        
        """
        If you have modified your roblox information with the verification bot configured with the server, you must run this command to refresh the roblox account that is bound to your discord account with `RoPerks`.
        """
                
        if ctx.author not in ctx.guild.premium_subscribers:
            embed=discord.Embed(title="You are currently not Boosting this server.", description=f"<:warningerrors:713782413381075536> Use `{ctx.prefix}help {ctx.command}` for more help.\n\n<:Join:718154643095683142>*Can't figure it out?: [__click here for our support server__](https://discord.gg/nG2ZUjPuF9)*", color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(ctx.cog, ctx))
            await ctx.send(embed=embed)
            return
        
        roblox_id = await self.bot.db_pool.fetchval(f'SELECT roblox_id FROM user_data WHERE guild_id=$1 AND discord_id=$2', ctx.guild.id, ctx.author.id)
        new_roblox_id = await darealmodule.Helping.get_discord_roblox(self, ctx.guild.id, ctx.author.id)
        
        if roblox_id == new_roblox_id:
            embed=discord.Embed(title="No changes to be made.", description=f"<:warningerrors:713782413381075536> The roblox accounts bound to `{await darealmodule.Helping.get_verification_sys(self, ctx.guild.id)}` and `{self.bot.user.name}` are the same.\n\n<:Join:718154643095683142>*Can't figure it out?: [__click here for our support server__](https://discord.gg/nG2ZUjPuF9)*", color=0x2f3136)
            embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(ctx.cog, ctx))
            await ctx.send(embed=embed)
            return
        
        await self.bot.db_pool.execute(f"UPDATE user_data SET roblox_id=$1 WHERE guild_id=$2 AND discord_id=$3", new_roblox_id, ctx.guild.id, ctx.author.id)
        
        embed=discord.Embed(description=f"<:check:711530148196909126> Successfully set `{new_roblox_id}` as your new account bound with `{self.bot.user.name}`.\n\n<:Join:718154643095683142>*Can't figure it out?: [__click here for our support server__](https://discord.gg/nG2ZUjPuF9)*")
        embed.color = 0x2f3136
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Configuration(bot))
