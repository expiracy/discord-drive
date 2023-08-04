import asyncio
import json
import logging
import os
import platform
import random
import sys

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context, bot


class StorageBot(commands.Bot):
    def __init__(self):
        try:
            with open(f"{os.path.dirname(__file__)}\\config.json", 'r') as json_file:
                self.config = json.load(json_file)

        except IOError as e:
            sys.exit(f"Could not load config: {e}")

        intents = discord.Intents.default()
        intents.message_content = True  # Only for testing

        super().__init__(
            command_prefix=self.config["prefix"],
            intents=intents,
        )

    def run(self, **kwargs):
        asyncio.run(self.load_cogs())
        super().run(token=self.config["token"])

    async def on_ready(self) -> None:
        print(f"Logged in as {self.user.name}")

        if self.config["sync_commands_globally"]:
            await self.tree.sync()

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user or message.author.bot:
            return

        print(message.content)

        await self.process_commands(message)

    async def load_cogs(self) -> None:
        for file in os.listdir(f"{os.path.dirname(__file__)}\\cogs"):
            if file.endswith(".py"):
                extension = file[:-3]

                if extension == "__init__":
                    continue

                try:
                    await self.load_extension(f"cogs.{extension}")
                    print(f"Loaded cog: {extension}")
                except Exception as e:
                    print(e)

