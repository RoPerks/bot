import discord
from discord import errors
from discord.ext import commands, tasks
import darealmodule
import asyncio
import datetime
import time
import asyncpg

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @tasks.loop(seconds=60)
    async def set_status(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="-help | -setup | -docs"))
        await asyncio.sleep(20)

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{len([m for m in self.bot.get_all_members()])} Members"))
        await asyncio.sleep(20)

        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"Stuck? discord.gg/nG2ZUjPuF9"))
        await asyncio.sleep(20)
        
                        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        
        if await self.bot.db_pool.fetchval('SELECT EXISTS (SELECT 1 FROM guild_dump WHERE guild_id=$1)', after.guild.id):

            premium_role = after.guild.premium_subscriber_role
            
            difference_role_add = list(set(after.roles) - set(before.roles))
            difference_role_subtract = list(set(before.roles) - set(after.roles))
            if difference_role_add and premium_role in difference_role_add:
                if not await self.bot.db_pool.fetchval('SELECT EXISTS (SELECT 1 FROM user_data WHERE guild_id=$1 AND discord_id=$2)', after.guild.id, after.id):
                    roblox_id = await darealmodule.Helping.get_discord_roblox(self, after.guild.id, after.id)
                    if roblox_id:
                        await self.bot.db_pool.execute(f"INSERT INTO user_data VALUES ($1, $2, $3)", after.guild.id, after.id, roblox_id)

            elif difference_role_subtract and premium_role in difference_role_subtract:
                if await self.bot.db_pool.fetchval('SELECT EXISTS (SELECT 1 FROM user_data WHERE guild_id=$1 AND discord_id=$2)', after.guild.id, after.id):
                    await self.bot.db_pool.execute(f"DELETE FROM user_data WHERE guild_id=$1 AND discord_id=$2", after.guild.id, after.id)



    @commands.Cog.listener()
    async def on_ready(self):

        self.set_status.start()

        for guild in self.bot.guilds:
            if await self.bot.db_pool.fetchval('SELECT EXISTS (SELECT 1 FROM guild_dump WHERE guild_id=$1)', guild.id):
                premium_user_ids = [user.id for user in guild.premium_subscribers]

                data = await self.bot.db_pool.fetch('SELECT * FROM user_data WHERE guild_id=$1', guild.id)
                logged_user_ids = [int(user['discord_id']) for user in data]

                need_to_be_removed = list(set(logged_user_ids) - set(premium_user_ids))
                need_to_be_added = list(set(premium_user_ids) - set(logged_user_ids))
                for user in need_to_be_removed:
                    if await self.bot.db_pool.fetchval('SELECT EXISTS (SELECT 1 FROM user_data WHERE guild_id=$1 AND discord_id=$2)', guild.id, user):
                        await self.bot.db_pool.execute(f"DELETE FROM user_data WHERE guild_id=$1 AND discord_id=$2", guild.id, user)
                for user in need_to_be_added:
                    if not await self.bot.db_pool.fetchval('SELECT EXISTS (SELECT 1 FROM user_data WHERE guild_id=$1 AND discord_id=$2)', guild.id, user):
                        roblox_id = await darealmodule.Helping.get_discord_roblox(self, guild.id, user)
                        if roblox_id:
                            await self.bot.db_pool.execute(f"INSERT INTO user_data VALUES ($1, $2, $3)", guild.id, user, roblox_id)


        print('[*] Logged in as')
        print('[*]', self.bot.user.name)
        print('[*]', self.bot.user.id)
        print('----------------------')


async def setup(bot):
    await bot.add_cog(Events(bot))
