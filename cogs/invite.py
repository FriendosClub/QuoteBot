import discord
from discord.ext import commands


class Invite:
    def __init__(self, bot):
        self.bot = bot
        self.perms = 117760

    @commands.command()
    async def invite(self, ctx):
        """Print a URL to invite QuoteBot to your server.
        """
        print(f"{ctx.author.id} requested an invite URL.")
        await ctx.send("https://discordapp.com/oauth2/authorize" +
                       f"?client_id={self.bot.user.id}&scope=bot" +
                       f"&permissions={self.perms}")


def setup(bot):
    bot.add_cog(Invite(bot))
