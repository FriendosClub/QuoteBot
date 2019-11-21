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
