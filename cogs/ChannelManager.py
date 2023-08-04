import discord
from discord.ext import commands
from discord.ext.commands import Context


class ChannelManager(commands.Cog, name="ChannelManager"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="test",
        description="Test command.",
    )
    async def test(self, context: Context) -> None:
        await context.send("test")

    @commands.hybrid_command(
        name="cc",
        description="Creates a channel.",
    )
    async def cc(self, context: Context, name: str):
        await self.create_channel(context, name)

    @commands.command()
    async def create_channel(self, context: Context, channel_name: str) -> None:
        """Creates a new text channel in the server."""
        guild = context.guild

        if not guild:
            return

        try:
            await guild.create_text_channel(name=channel_name)
            await context.send(f"Channel '{channel_name}' has been created.")
        except discord.Forbidden:
            await context.send("I don't have the necessary permissions to create a channel.")
        except discord.HTTPException:
            await context.send("Failed to create the channel. Please try again later.")


async def setup(bot):
    await bot.add_cog(ChannelManager(bot))
