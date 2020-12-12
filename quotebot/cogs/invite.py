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


class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.perms = 117760

    @commands.command()
    async def invite(self, ctx):
        """Print a URL to invite QuoteBot to a server.
        """
        print(f"{ctx.author.name}#{ctx.author.discriminator} requested an invite URL.")
        await ctx.send("Use this URL to invite QuoteBot to your server: " +
                       "https://discordapp.com/oauth2/authorize" +
                       f"?client_id={self.bot.user.id}&scope=bot" +
                       f"&permissions={self.perms}")


def setup(bot):
    bot.add_cog(Invite(bot))
