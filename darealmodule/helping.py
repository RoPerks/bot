from base64 import urlsafe_b64decode
import datetime
import secrets
import json

import darealmodule


class Helping():

    def __init__(self):
        self.now = datetime.datetime.now()

    def get_time_in_gmt(self):

        if len(str(self.now.minute)) == 1:
            x = f"0{self.now.minute}"
        else:
            x = self.now.minute

        return f'{self.now.hour}:{x}'

    def get_footer(self, ctx):
        return f'[-] Invoked by {ctx.author} @ {Helping().get_time_in_gmt()}'


    async def get_discord_roblox(self, guild_id, discord_id):
        verification_sys = await darealmodule.Helping.get_verification_sys(self, guild_id)
        if verification_sys == 'rover':
            return await darealmodule.Helping.get_rover_verification(self, discord_id)
        elif verification_sys == 'rowifi':
            return await darealmodule.Helping.get_rowifi_verification(self, discord_id, guild_id)
        elif verification_sys == 'bloxlink':
            return await darealmodule.Helping.get_bloxlink_verification(self, discord_id)
        
    async def get_verification_sys(self, guild_id):
        return await self.bot.db_pool.fetchval(f'SELECT verification_sys FROM guild_dump WHERE guild_id=$1', guild_id)

    async def get_bloxlink_verification(self, discord_id):
        headers = {'api-key': 'a9566e95-2bc8-4b5a-801a-e74ba0a3f429'}
        response = await self.bot.web_client.get(f"https://v3.blox.link/developer/discord/{discord_id}", headers=headers)
        json = await response.json()
        if response.status != 200 or len(json) == 0:
            return None
        return int(json['user']['primaryAccount'])
        
    async def get_rover_verification(self, discord_id):
        response = await self.bot.web_client.get(f'https://verify.eryn.io/api/user/{discord_id}')
        json = await response.json()
        if response.status != 200:
            return None
        return json['robloxId']
        
    async def get_rowifi_verification(self, discord_id, guild_id):
        response = await self.bot.web_client.get(f'https://api.rowifi.xyz/v2/guilds/{guild_id}/members/{discord_id}', headers={'Authorization': 'Bot mtvxkKokrgjudNMi'})
        if response.status != 200:
            return None
        data = await response.read()
        js = json.loads(data)
        return js['roblox_id']

    async def generate_api_key(self):
        existing_api_keys = await self.bot.db_pool.fetch(f'SELECT api_key FROM guild_dump')
        existing_api_keys_sanatized = []
        for record in existing_api_keys:
            existing_api_keys_sanatized.append(record['api_key'])
        while True:
            token = secrets.token_urlsafe(16)
            if token not in existing_api_keys_sanatized:
                break
            
        return token
        
    async def get_api_key(self, ctx):
        api_key = await self.bot.db_pool.fetchval(f'SELECT api_key FROM guild_dump WHERE guild_id=$1', ctx.guild.id)
        return api_key
