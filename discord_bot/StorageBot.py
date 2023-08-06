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

from storage.File import File
from storage.Folder import Folder


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

    async def upload_file(self, file, guild_id):
        guild = self.bot.get_guild(guild_id)

        for channel in guild.channels:
            if channel.name == "files":
                message = await channel.send(file=discord.File(file))
                return message.id

        return -1

    async def login(self):
        await self.bot.login(self.config["token"])
        print(f"Logged in as {self.bot.user}")

    async def connect(self):
        await self.bot.connect()

    async def create_folder(self, guild_id: int, folder_name: str) -> int:
        guild = self.bot.get_guild(guild_id)

        if not guild:
            return -1

        if folder_name in set(map(lambda c: str(c), guild.text_channels)):
            return -1

        channel = await guild.create_text_channel(name=folder_name)
        return channel.id


