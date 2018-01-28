import discord
from discord.ext import commands


def owner_or_admin(ctx):
    """Check to see if the user invoking the command is owner OR admin.
    Thanks to noodle#0001 on the discord.py server for this one.
    """
    async def predicate(ctx):
        return any([ctx.channel.permissions_for(ctx.author).manage_guild,
                    (str(ctx.author.id) in trustedusers)])
    return commands.check(predicate)


class Config:
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.group(invoke_without_command=True,
                    aliases=['quotechannel', 'qc'])
    async def quote_channel(self, ctx):
        """Base for 'qc set' and 'qc get'. See 'help quote_channel'.
        """
        await ctx.send(f"Use `{ctx.command.qualified_name} get` or " +
                       f"`{ctx.command.qualified_name} set <channel mention>`")

    @commands.guild_only()
    @commands.check(owner_or_admin)
    @quote_channel.command(name='set')
    async def qc_set(self, ctx, channel: discord.TextChannel):
        """Set the text channel all quoted messages for a guild are embedded in.

        Args:
            channel (discord.TextChannel): Channel mention, i.e. #general.
        """
        if self.bot.dbh.set_quote_channel(ctx.guild.id, channel.id):
            print(f"{ctx.author.id} set quote channel for {ctx.guild.id} to " +
                  f"{channel.id}")
            await ctx.send(f"Quote channel for {ctx.guild.name} " +
                           f"is now {channel.mention}.")
        else:
            await ctx.send("Unable to update channel.")

    @qc_set.error
    async def qc_set_error_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("That channel doesn't exist.")
        else:
            raise error

    @commands.guild_only()
    @quote_channel.command(name='get')
    async def qc_get(self, ctx):
        """Gets the channel quoted messages are currently sent to.
        """
        qc_id = self.bot.dbh.get_quote_channel(ctx.guild.id)

        if qc_id:
            qc = ctx.guild.get_channel(qc_id)
        else:
            await ctx.send("An admin hasn't set the quote channel yet.")
            return

        if qc:
            await ctx.send(f"The quote channel for {ctx.guild.name} is " +
                           f"{qc.mention}.")
        else:
            await ctx.send("It looks like the quote channel was deleted. " +
                           "Ask an admin to set a new one with " +
                           "`qc set #channel`.")


def setup(bot):
    bot.add_cog(Config(bot))
