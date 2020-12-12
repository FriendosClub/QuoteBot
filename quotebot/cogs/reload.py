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


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def reload_cog(self, cog: str):
        """Reloads a specific cog. Makes development easy.

        Args:
            cog (str): Name of the cog, e.g. `cogs.quote`.
        """
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            print(f"Error unloading {cog}")
            raise e

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            print(f"Error loading {cog}")
            raise e
        else:
            print(f"Reloaded {cog}")

    @commands.is_owner()
    @commands.group(invoke_without_command=True, name='reload')
    async def full_reload(self, ctx, *cogs):
        """[Owner only] Reloads every cog or specified cogs.

        Args:
            *cogs: List of cogs to reload.
        """
        prefix = ""
        if not cogs:
            cogs = self.bot.ext_names
        else:
            prefix = 'cogs.'

        for cog in cogs:
            self.reload_cog(prefix + cog)

        await ctx.send("Reloaded.")


def setup(bot):
    bot.add_cog(Reload(bot))
