import discord
from discord.ext import commands


class ReloadCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.group(invoke_without_command=True, name='reload')
    async def full_reload(self, ctx):
        load_count = 0

        for extension in self.bot.ext_names:
            try:
                self.bot.unload_extension(extension)
            except Exception as e:
                await ctx.send(f"Failed to unload extension {extension}.")
                raise e

        for extension in self.bot.ext_names:
            try:
                self.bot.load_extension(extension)
            except Exception as e:
                await ctx.send(f"Failed to load extension {extension}")
                raise e
            else:
                load_count += 1

        await ctx.send(f"Reloaded {load_count} extensions.")

    @commands.is_owner()
    @full_reload.command(name='ext')
    async def reload_ext(self, ctx, ext_name: str):
        try:
            self.bot.unload_extension(f'cogs.{ext_name}')
        except Exception as e:
            await ctx.send(f"Failed to unload cogs.{ext_name}.")
            raise e

        try:
            self.bot.load_extension(f'cogs.{ext_name}')
        except Exception as e:
            await ctx.send(f"Failed to load cog cogs.{ext_name}")
            raise e
        else:
            await ctx.send(f"Reloaded cogs.{ext_name}.")


def setup(bot):
    bot.add_cog(ReloadCog(bot))
