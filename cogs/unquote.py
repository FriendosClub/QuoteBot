import discord
from discord.ext import commands


class Unquote:
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def unquote(self, ctx, *msg_ids):
        """Remove the specified message from the quote channel.

        Args:
            *msg_ids: ID(s) of the quotes to remove.
        """
        if not msg_ids:
            await ctx.send("Please specify at least one message ID.")
            return

        quote_channel_id = self.bot.dbh.get_quote_channel(ctx.guild.id)
        quote_channel = self.bot.get_channel(quote_channel_id)

        if quote_channel is None:
            await ctx.send("You haven't specified a quote channel! " +
                           "You can set one with `qc set #channel`.")
            return

        deleted_count = 0
        for msg_id in msg_ids:
            try:
                msg = await quote_channel.get_message(msg_id)
            except discord.NotFound:
                await ctx.send("No message exists with that ID.")
                continue
            except discord.Forbidden:
                await ctx.send("I can't access that channel.")
                continue
            except discord.HTTPException as he:
                # TODO: Maybe add conditionals for different error codes
                await ctx.send(f"Got error code {he.status} " +
                               "trying to retrieve message.")
                raise he
                continue

            try:
                await msg.delete()
            except Exception as e:
                await ctx.send(f"Error removing message ID {msg.id}.")
                raise e
            else:
                deleted_count += 1
                self.bot.dbh.update_quote_count(ctx.guild.id, -1)

        await ctx.send(f"Deleted {deleted_count} quotes.")


def setup(bot):
    bot.add_cog(Unquote(bot))
