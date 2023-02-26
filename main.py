import asyncio
import logging
import logging.handlers
from dotenv import load_dotenv
import os

from typing import List, Optional

import asyncpg
import discord
from discord import app_commands
from discord.ext import commands
from aiohttp import ClientSession

from cogs.info import EmbedHelpCommand


load_dotenv()

class Bot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        db_pool: asyncpg.Pool,
        web_client: ClientSession,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.db_pool = db_pool
        self.web_client = web_client
        self.initial_extensions = initial_extensions
        # self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:

        for extension in self.initial_extensions:
            await self.load_extension(extension)
            
        await self.tree.sync()
        
        self.std_error = await self.fetch_channel(1044744775636615279)

async def main():

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    try:
        pool_ = await asyncpg.create_pool(host=os.getenv('DATABASE_HOST'), database="RoPerks", user="postgres", password=os.getenv('DATABASE_PASSWORD'))
    except:
        pool_ = await asyncpg.create_pool(host="localhost", database="RoPerks", user="postgres", password=os.getenv('DATABASE_PASSWORD'))
        
    async with ClientSession() as our_client, pool_ as pool:
        
        intents = discord.Intents.all()

        async with Bot(command_prefix=["-", "sudo."],
                        case_insensetive=True,
                        help_command=EmbedHelpCommand(),
                        intents=intents,

                        db_pool=pool, 
                        web_client=our_client, 
                        initial_extensions=['cogs.configuration', 'cogs.developer', 'cogs.info', 'jishaku', 'events.background', 'events.errors'],
                        ) as bot:

            await bot.start(os.getenv('TOKEN'))


asyncio.run(main())
