import discord
from discord.ext import commands


class QuoteCog:
    def __init__(self, bot):
        self.bot = bot

    # TODO: Figure out how to process `channel` since it is now a named argument.
    @commands.guild_only()
    @commands.command()
    async def quote(self, ctx, *msg_ids, channel: discord.TextChannel = None):
        """Quote a message.

        Args:
            msg_id (int): The ID of the message (... > Copy ID)
            channel (discord.TextChannel, optional): Which channel to search.
        """
        if not msg_ids:
            await ctx.send("Please specify at least one message ID.")
            return

        quote_channel_id = self.bot.dbh.get_quote_channel(ctx.guild.id)
        quote_channel = self.bot.get_channel(quote_channel_id)

        if quote_channel is None:
            await ctx.send("You haven't specified a quote channel! " +
                           "You can set one with `set_quote_channel #channel`.")
            return

        if not channel:
            channel = ctx.message.channel

        # TODO: Refactor this loop
        for msg_id in msg_ids:
            try:
                msg = await channel.get_message(msg_id)
            except discord.NotFound:
                await ctx.send("No message exists with that ID.")
                continue
            except discord.Forbidden:
                await ctx.send("I don't have permission to access that channel.")
                continue
            except discord.HTTPException as he:
                await ctx.send(f"Got error code {he.status} trying to retrieve message.")
                continue

            e = discord.Embed(description=msg.content, color=msg.author.color)
            e.set_author(name=msg.author.display_name,
                         icon_url=msg.author.avatar_url_as(size=64))

            # TODO: Handle up to 10 possible attachments
            # TODO: Handle attachments that aren't images
            if msg.attachments and hasattr(msg.attachments[0], 'height'):
                e.set_image(url=msg.attachments[0].url)

            self.bot.dbh.update_quote_count(ctx.guild.id)

            await quote_channel.send(embed=e)

        # TODO: Print correct number (i.e. decrement by failed number of msgs)
        await ctx.send(f"Quoted {len(msg_ids)} messages.")

    @quote.error
    async def quote_error_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            print(error)
            await ctx.send("That channel doesn't exist!")


def setup(bot):
    bot.add_cog(QuoteCog(bot))
