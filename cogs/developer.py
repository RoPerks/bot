import discord
from discord.ext import commands
import time
import sys
import os
import darealmodule
import asyncio
import requests
from discord import app_commands

import traceback

from discord import ui



class Developer(commands.Cog):
    """These commands have been reserved for the ownership team to streamline development."""

    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(description="Owner only.", help='Loads specified cog.')
    @commands.is_owner()
    async def load(self, ctx, extension):
        """
        Loads the given cog, if it already loaded it will raise an error
        """
        try:
            await self.bot.load_extension(f"cogs.{extension}")
        except commands.errors.ExtensionAlreadyLoaded:
            await ctx.send(f"<:rcross:711530086251364373> | **Cog already loaded: `{extension}`**")
        else:
            await ctx.send(f"<a:anime_tick:725336519904067615> | **Loaded Cog: `{extension}`**")

    @commands.command(description="Owner only.", help='Reloads specified cog.')
    @commands.is_owner()
    async def reload(self, ctx, extension):
        """
        Reloads the given cog, if an error is raised it will not load again
        """
        try:
            await self.bot.unload_extension(f"cogs.{filename[:-3]}")
        except commands.errors.ExtensionNotLoaded:
            await ctx.send(f"<:rcross:711530086251364373> | **Cog not loaded: `{extension}`**")
        else:
            await self.bot.load_extension(f"cogs.{filename[:-3]}")
            await ctx.send(f"<a:anime_tick:725336519904067615> | **Realoded Cog: `{extension}`**")

    @commands.command(description="Owner only.", help='Unloads specified cog.')
    @commands.is_owner()
    async def unload(self, ctx, extension):
        """
        Unloads the given cog, if it already unloaded it will raise an error.
        """
        try:
            await self.bot.unload_extension(f"cogs.{extension}")
        except commands.errors.ExtensionNotLoaded:
            await ctx.send(f"<:rcross:711530086251364373> | **Cog not loaded: `{extension}`**")
        else:
            await ctx.send(f"<a:anime_tick:725336519904067615> | **Unloaded Cog: `{extension}`**")

    @commands.command(description="Owner only.", help='Reloads all cogs.')
    @commands.is_owner()
    async def r(self, ctx):
        """
        Reloads all cogs buy unloading and loading each cog, if an error is raised the cog will not be loaded.
        """

        embed=discord.Embed(title="a", color=0x2f3136)
        # embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
        # await ctx.send(embed=embed)
        # return
        description=""
        loaded=0
        not_loaded=0
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.bot.unload_extension(f"cogs.{filename[:-3]}")
                except commands.errors.ExtensionNotLoaded:
                    description += f"<:warningerrors:713782413381075536> | **Cog not loaded: `{filename[:-3]}`**\n"
                    not_loaded+=1
                else:
                    await self.bot.load_extension(f"cogs.{filename[:-3]}")
                    description += f"<a:anime_tick:725336519904067615> | **Realoded Cog: `{filename[:-3]}`**\n"
                    loaded+=1

                    # await ctx.send(f"<a:anime_tick:725336519904067615> | **Realoded Cog: `{filename[:-3]}`**")
        #await ctx.send(f"<a:anime_tick:725336519904067615> | `Reloaded the cogs`")
        embed.title=f'{loaded} modules where loaded & {not_loaded} modules where not loaded.'
        embed.description=description
        embed.set_footer(icon_url=ctx.author.avatar.replace(format="png"), text=darealmodule.Helping.get_footer(self, ctx))
        await ctx.send(embed=embed)

    @commands.command(description="Owner only.", help='Shows all cogs.')
    @commands.is_owner()
    async def cogs(self, ctx):
        """
        Sends a list of all loaded cogs, events and unloaded cogs will be skipped.
        """
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.send(f"`{filename[:-3]}`")


    @commands.group(aliases=['dm'], help='Bots mode respective to the subcommand.')
    @commands.is_owner()
    async def debugmode(self, ctx):
        """
        Unloads/Reloads the error handler file, respective to the subcommand, meaning errors being handled will not be sent.
        """
        pass
        # await self.bot.unload_extension(f"events.errors")
        #
        # await ctx.send(f"<a:anime_tick:725336519904067615> | **Bot has been changed to debuging mode.**")

    @debugmode.command(name='-on', help='Changes the bot to debugmode.')
    async def _on(self, ctx):
        """
        Unloads the error handler file
        """
        try:
            await self.bot.unload_extension(f"events.errors")
            await ctx.send(f"<a:anime_tick:725336519904067615> | **Bot has been changed to debuging mode.**")
        except:
            await ctx.send(f"<:rcross:711530086251364373> | **The bot is already in debug mode.**")

    @debugmode.command(name='-off', help='Turns debug mode off.')
    async def _off(self, ctx):
        """
        Loads the error handler file.
        """
        try:
            await self.bot.load_extension(f"events.errors")
            await ctx.send(f"<a:anime_tick:725336519904067615> | **Debuging mode has been turned off.**")
        except:
            await ctx.send(f"<:rcross:711530086251364373> | **Debug mode is already off.**")

    @commands.is_owner()
    @commands.command(description="Submit feedback")
    async def test(self, ctx):
        
        class Feedback(discord.ui.Modal, title='Feedback'):
            # Our modal classes MUST subclass `discord.ui.Modal`,
            # but the title can be whatever you want.

            # This will be a short input, where the user can enter their name
            # It will also have a placeholder, as denoted by the `placeholder` kwarg.
            # By default, it is required and is a short-style input which is exactly
            # what we want.
            name = discord.ui.TextInput(
                label='Name',
                placeholder='Your name here...',
            )

            # This is a longer, paragraph style input, where user can submit feedback
            # Unlike the name, it is not required. If filled out, however, it will
            # only accept a maximum of 300 characters, as denoted by the
            # `max_length=300` kwarg.
            feedback = discord.ui.TextInput(
                label='What do you think of this new feature?',
                style=discord.TextStyle.long,
                placeholder='Type your feedback here...',
                required=False,
                max_length=300,
            )

            async def on_submit(self, interaction: discord.Interaction):
                await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

            async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
                await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

                # Make sure we know what the error actually is
                traceback.print_tb(error.__traceback__)

        
        class Confirm(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.value = None

            # When the confirm button is pressed, set the inner value to `True` and
            # stop the View from listening to more input.
            # We also send the user an ephemeral message that we're confirming their choice.
            @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
            async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_modal(Feedback())
                self.value = True
                self.stop()

            # This one is similar to the confirmation button except sets the inner value to `False`
            @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
            async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.send_message('Cancelling', ephemeral=True)
                self.value = False
                self.stop()

        view = Confirm()
        await ctx.send('Do you want to continue?', view=view)

        await view.wait()
        if view.value is None:
            print('Timed out...')
        elif view.value:
            print('Confirmed...')
        else:
            print('Cancelled...')
        



            
async def setup(bot):
    await bot.add_cog(Developer(bot))