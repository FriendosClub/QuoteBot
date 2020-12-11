# QuoteBot - A Discord bot for archiving your favorite messages.
# Copyright (C) 2020  Ralph Drake

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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


class Config(commands.Cog):
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
            print(f"{ctx.author.name}#{ctx.author.discriminator} " +
                  f"set quote channel for {ctx.guild.name} ({ctx.guild.id}) to " +
                  f"#{channel.name} ({channel.id})")
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
