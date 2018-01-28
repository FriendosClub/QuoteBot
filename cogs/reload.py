import discord
from discord.ext import commands


class Reload:
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
