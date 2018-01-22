import discord
from discord.ext import commands


class ConfigCog:
    def __init__(self, bot):
        self.bot = bot

    # TODO: Error handler for incorrect channel
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def set_quote_channel(self, ctx, channel: discord.TextChannel):
        """Set the text channel all quoted messages for a guild are embedded in.

        Args:
            channel (discord.TextChannel): The channel's mention, i.e. #general.
        """
        if self.bot.dbh.set_quote_channel(ctx.guild.id, channel.id):
            await ctx.send(f"Quote channel for {ctx.guild.name} is now {channel.mention}.")
        else:
            await ctx.send("Unable to update channel.")


def setup(bot):
    bot.add_cog(ConfigCog(bot))
