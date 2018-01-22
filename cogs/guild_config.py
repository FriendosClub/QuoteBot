import discord
from discord.ext import commands


class ConfigCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.group(invoke_without_command=True,
                    aliases=['quotechannel', 'qc'])
    async def quote_channel(self, ctx):
        await ctx.send(f"Use `{ctx.command.qualified_name} get` or " +
                       f"`{ctx.command.qualified_name} set <channel mention>`")

    # TODO: Error handler for incorrect channel
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @quote_channel.command(name='set')
    async def qc_set(self, ctx, channel: discord.TextChannel):
        """Set the text channel all quoted messages for a guild are embedded in.

        Args:
            channel (discord.TextChannel): Channel mention, i.e. #general.
        """
        if self.bot.dbh.set_quote_channel(ctx.guild.id, channel.id):
            await ctx.send(f"Quote channel for {ctx.guild.name} is now {channel.mention}.")
        else:
            await ctx.send("Unable to update channel.")

    @qc_set.error
    async def qc_set_error_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("That channel doesn't exist.")

    @commands.guild_only()
    @quote_channel.command(name='get')
    async def qc_get(self, ctx):
        qc_id = self.bot.dbh.get_quote_channel(ctx.guild.id)

        if qc_id:
            qc = ctx.guild.get_channel(qc_id)
        else:
            await ctx.send("An admin hasn't set the quote channel yet.")
            return

        if qc:
            await ctx.send(f"The quote channel for {ctx.guild.name} is +"
                           f"{qc.mention}.")
        else:
            await ctx.send("It looks like the quote channel was deleted. " +
                           "Ask an admin to set a new one with " +
                           "`qc set #channel`.")


def setup(bot):
    bot.add_cog(ConfigCog(bot))
