import discord
from discord.ext import commands


class StatsCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def stats(self, ctx):
        """Print some QuoteBot statistics in chat.
        """
        local_qc = self.bot.dbh.get_quote_count(ctx.guild.id)
        await ctx.send(f"I've quoted {local_qc} messages from {ctx.guild.name}")


def setup(bot):
    bot.add_cog(StatsCog(bot))
