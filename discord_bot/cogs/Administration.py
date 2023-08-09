import requests
from discord.ext import commands
from discord.ext.commands import Context

from storage.Registration import Registration


# Here we name the cog and create a new class for the cog.
class Administration(commands.Cog, name="Administration"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="register_server",
        description="Register this server as a storage server.",
    )
    async def register_server(self, context: Context, password: str):
        file_channel = await context.guild.create_text_channel(name="files")
        registration = Registration(context.author.name, password, context.guild.id, file_channel.id)

        response = requests.post("http://127.0.0.1:5000/api/register", json=registration.to_json())
        print(response)

        return await context.send(f"Successfully registered server!\nUsername: {registration.username}\nPassword: {registration.password}")


async def setup(bot):
    await bot.add_cog(Administration(bot))
