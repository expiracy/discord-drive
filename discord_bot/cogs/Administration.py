import asyncio
import threading
import time

import aiohttp
import requests
from discord.ext import commands
from discord.ext.commands import Context
from quart import request

from database.DatabaseManager import DatabaseManager
from storage.Registration import Registration


# Here we name the cog and create a new class for the cog.
class Administration(commands.Cog, name="Administration"):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def register_in_database(username, password, guild_id, channel_id):
        database = DatabaseManager()
        directory_id = database.add_directory("files", None)
        database.register_user(username, password, guild_id, channel_id, directory_id)

    @commands.hybrid_command(
        name="register_server",
        description="Register this server as a storage server.",
    )
    async def register(self, context: Context, password: str):
        file_channel = await context.guild.create_text_channel(name="files")

        threading.Thread(target=Administration.register_in_database,
                         args=(context.author.name, password, context.guild.id, file_channel.id)).start()

        return await context.send(f"SERVER REGISTERED\nUsername: {context.author.name}\nPassword: {password}")


async def setup(bot):
    await bot.add_cog(Administration(bot))
