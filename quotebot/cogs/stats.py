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


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def stats(self, ctx):
        """Print some QuoteBot statistics in chat.
        """
        e = discord.Embed(color=ctx.guild.me.color)
        e.set_author(name=f'{ctx.guild.me.display_name} Statistics',
                     url='https://github.com/RalphORama/QuoteBot',
                     icon_url=self.bot.user.avatar_url_as(size=128))

        e.add_field(name=f'Messages quoted from {ctx.guild.name}:',
                    value=self.bot.dbh.get_quote_count(ctx.guild.id),
                    inline=False)
        e.add_field(name='Total messages quoted:',
                    value=self.bot.dbh.get_quote_count_global(),
                    inline=False)
        e.add_field(name='Number of servers joined:',
                    value=len(self.bot.guilds),
                    inline=False)

        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Stats(bot))
