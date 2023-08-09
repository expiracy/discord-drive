import asyncio
import json
import logging
import os
import platform
import random
import sys

import discord
from discord import Client
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context, bot
from discord_bot.cogs import Administration

from storage.File import File
from storage.Folder import Folder
from storage.Registration import Registration


class StorageBot:

    def __init__(self):
        try:
            with open(f"{os.path.dirname(__file__)}\\..\\resources\\config.json", 'r') as json_file:
                self.config = json.load(json_file)

        except IOError as e:
            sys.exit(f"Could not load config: {e}")

        # Setting the intents

        intents = discord.Intents.default()
        intents.message_content = True

        self.bot = commands.Bot(
            command_prefix="!",
            intents=intents,

        )

        asyncio.run(self.load_cogs())

    async def load_cogs(self):
        for file in os.listdir(f"{os.path.dirname(__file__)}\\cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.bot.load_extension(f"discord_bot.cogs.{extension}")
                    print(f"Loaded {extension}")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(exception)

    async def get_message(self, message_id, guild_id=1136677852796952586, channel_id=1137850799523889314):
        guild = self.bot.get_guild(guild_id)

        channel = guild.get_channel(channel_id)

        return await channel.fetch_message(message_id)

    async def upload_file(self, file, guild_id=1136677852796952586):
        guild = self.bot.get_guild(guild_id)

        for channel in guild.channels:
            if channel.name == "files":
                message = await channel.send(file=discord.File(file))
                return message.id

        return -1

    async def login(self):
        await self.bot.login(self.config["token"])
        print(f"Logged in as {self.bot.user}")
        if self.config["sync_commands_globally"]:
            await self.bot.tree.sync()

    async def connect(self):
        await self.bot.connect()

    async def send_message(self, message, guild_id=1136677852796952586, channel_id=1137850799523889314):
        guild = self.bot.get_guild(guild_id)
        channel = guild.get_channel(channel_id)

        message = await channel.send(message)
        return message.id

    async def get_file(self, message_id=1137904409108566016, guild_id=1136677852796952586,
                       channel_id=1137850799523889314):
        guild = self.bot.get_guild(guild_id)

        channel = guild.get_channel(channel_id)

        message = await channel.fetch_message(message_id)

        return message.attachments[0]

    '''
    async def create_folder(self, guild_id: int, folder_name: str) -> int:
        guild = self.bot.get_guild(guild_id)

        channel = await guild.create_text_channel(name=folder_name)
        return channel.id
    '''
