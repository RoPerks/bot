from __future__ import annotations
import discord
from discord.ext import commands
import time
import datetime
import darealmodule

class EmbedHelpCommand(commands.HelpCommand):

    COLOUR = 0x2f3136
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verify_checks = False
        self.__doc__ = 'asd'

    async def command_callback(self, ctx, *, command=None):

        await self.prepare_help_command(ctx, command)
        bot = ctx.bot

        if command is None:
            mapping = self.get_bot_mapping()
            return await self.send_bot_help(mapping)

        command = command.lower().title()
        cog = bot.get_cog(command)
        if cog is not None:
            return await self.send_cog_help(cog)

        command = command.lower()        
        maybe_coro = discord.utils.maybe_coroutine

        keys = command.split(' ')
        cmd = bot.all_commands.get(keys[0])
        if cmd is None:
            string = await maybe_coro(self.command_not_found, self.remove_mentions(keys[0]))
            return await self.send_error_message(string)

        for key in keys[1:]:
            try:
                found = cmd.all_commands.get(key)
            except AttributeError:
                string = await maybe_coro(self.subcommand_not_found, cmd, self.remove_mentions(key))
                return await self.send_error_message(string)
            else:
                if found is None:
                    string = await maybe_coro(self.subcommand_not_found, cmd, self.remove_mentions(key))
                    return await self.send_error_message(string)
                cmd = found

        if isinstance(cmd, discord.ext.commands.core.Group):
            return await self.send_group_help(cmd)
        else:
            return await self.send_command_help(cmd)

    def get_ending_note(self):
        now = datetime.datetime.now()
        if len(str(now.minute)  ) == 1:
            x = f"0{now.minute}"
        else:
            x = now.minute
        return f'[-] Invoked by {self.context.author} @ {now.hour}:{x}'.format(self.context.clean_prefix, self.invoked_with)

    def get_opening_note(self):
        return f'```md\n * {self.context.clean_prefix}{self.invoked_with} [command | module] for help on a command/module.```'

    def get_command_signature(self, command):
        return '{0.qualified_name} {0.signature}'.format(command)
    def get_command_signature_name(self, command):
        return '{0.qualified_name}'.format(command)
    def get_author_icon(self):
        return f'{self.context.author.replace(format="png")}'
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='<:balloons:714891302763757629> HELP PANNEL <:balloons:714891302763757629>', description=self.get_opening_note(), colour=self.COLOUR)
        description = self.context.bot.description
        if description:
            embed.description = description
        cogs = ""
        for cog in self.context.bot.cogs.values():
            # if cog == 'OwnerOnly':
            #     cog=''
            try:
                # cogs += '• '
                cogs += f'• {cog.icon}'
                cogs += ' '
                cogs += f'{cog.qualified_name}'
                cogs += '\n'
            except AttributeError:
                pass

        cogs += '\n\n'
            # name = 'No Category' if cog is None else cog.qualified_name
            # filtered = await self.filter_commands(commands, sort=True)
            # if filtered:
            #     value = '\u2002'.join(f'`{c.name}`' for c in commands)
            #     if cog:
            #         value = '{0}'.format(value)
        about=f"""
*Dev* *-* *`@lolkm8#6312`, `644648271901622283`*
<:catbox:719527304476491858>__*[Click here to view official documentation!](https://roperks.tech/docs)*__
<:Invite:718152781747453952>__*[Click here to invite the bot to your server!](https://discord.com/api/oauth2/authorize?client_id=1002704047721160804&permissions=517543889984&scope=bot)*__
<:Join:718154643095683142>__*[Click here to join the support server!](https://discord.gg/nG2ZUjPuF9)*__
        """
        embed.add_field(name='**Enabled Modules**', value=cogs, inline=True)
        embed.add_field(name='**About**', value=about, inline=True)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error):
        embed=discord.Embed(title="That command or module was not found.", description=f'<:warningerrors:713782413381075536> Please use `{self.context.clean_prefix}{self.invoked_with}` to see a full list of commands..', color=0x2f3136)
        embed.set_footer(icon_url=self.context.author.replace(format="png"), text=darealmodule.Helping.get_footer(self, self.context))
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):

        cmds=""
        embed = discord.Embed(title=f'{(cog.qualified_name).upper()} MODULE', colour=self.COLOUR)
        # if cog.description:
        #     embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            cmds += f"`{(self.get_command_signature_name(command)).strip()}`"
            cmds += f" - "
            if self.get_command_signature_name(command).strip() == 'help':
                cmds+='Shows this message'
            else:
                cmds += f'{command.help.strip()}'
            cmds += '\n'
        embed.add_field(name=f'**{cog.__doc__}**', value=cmds, inline=False)
        embed.set_thumbnail(url=cog.thumbnail)
        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        self.verify_checks=False
        embed = discord.Embed(title=self.get_command_signature(group), colour=self.COLOUR)
        if group.callback.__doc__:
            docstring = group.callback.__doc__.replace('{{prefix}}', self.context.clean_prefix)
            embed.description = docstring

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(name=self.get_command_signature(command), value=command.short_doc, inline=False)

        if len(group.aliases) != 0:
            aliases = ""
            for i in group.aliases:
                aliases+=f'`{i}`'
                aliases+=f'‏‏‎ ‎‏‏‎ ‎'
            embed.add_field(name='**Aliases**', value=aliases, inline=False)

        embed.set_thumbnail(url=group.cog.thumbnail)
        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    send_command_help = send_group_help

class Info(commands.Cog):

    """This Module allows give you reletive data about this bot."""
 
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = EmbedHelpCommand()
        bot.help_command.cog = self
        self.bot = bot
        self.icon = "<:Profilenot:718137089434189825>"
        self.thumbnail = 'https://cdn.discordapp.com/attachments/801951909455724566/870356895100198952/433846.png'

    @commands.command(aliases=['p'], help="Displays the average webstock latency.")
    async def ping(self, ctx):
        """
        Displays the average webstock latency averaged from 3 api requests.

        __Extra__
        Latency has no association to your personal networks, it pertains to the time it takes for the server and bot to communicate with eachother.
        """

        embed=discord.Embed(title="PONG", color=0x2f3136)
        embed.add_field(name=f"Average websocket latency", value=f"<:Info:718139261328556032> | `{round(self.bot.latency*1000)}`", inline=False)
        embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
        await ctx.send(embed=embed)


    @commands.command(help="Returns basic api usage and documentation.")
    async def docs(self, ctx):
        """
        Returns basic api usage and documentation.
        """

        await ctx.message.add_reaction('<a:loading:716280480579715103>')
                
        embed=discord.Embed(color=0x2f3136)
        embed.add_field(name=f"Docs", value=f"<:catbox:719527304476491858> __*[Click here to view official documentation!](https://roperks.tech/docs)*__", inline=False)
        embed.add_field(name=f"Basic Usage", value="```md\nhttps://roperks.tech/api/nitro_status/{roblox-id}?api_key={api-key}```\n`{roblox-id}` - The roblox ID of the person you intend to check for nitro.\n`{api-key}` - API-KEY given from the key command.", inline=False)
        embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
        await ctx.message.clear_reactions()
        await ctx.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(Info(bot))
