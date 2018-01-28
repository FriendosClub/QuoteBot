import discord
from discord.ext import commands


class Ping:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Simple command to ensure the bot is working.
        """
        await ctx.send("Pong!")


def setup(bot):
    bot.add_cog(Ping(bot))
