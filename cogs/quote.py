import discord
from discord.ext import commands


class QuoteCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def quote(self, ctx, *msg_ids):
        """Quote a message.

        Args:
            *msg_ids: Numreic IDs for messages to quote

        Returns:
            TYPE: Description
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

        # ctx.other_channel is specified in the `quote_from` function.
        if hasattr(ctx, 'other_channel'):
            channel = ctx.other_channel
        else:
            channel = ctx.message.channel

        # Counter for successful quotes
        num_quoted = 0

        for msg_id in msg_ids:
            try:
                msg = await channel.get_message(msg_id)
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
                continue

            # Users who left the server have no attribute 'color'
            if hasattr(msg.author, 'color'):
                author_color = msg.author.color
            else:
                author_color = discord.Colour(0xFFFFFF)

            e = discord.Embed(description=msg.content, color=author_color)
            e.set_author(name=msg.author.display_name,
                         icon_url=msg.author.avatar_url_as(size=128))

            atch_urls = ""
            if msg.attachments:
                # Debugging
                print(f"Found {len(msg.attachments)} attachments.")
                if (
                    # If there's only one attachment and it's an image,
                    # attach it to the embed.
                    msg.attachments[0].height and len(msg.attachments) == 1
                ):
                    e.set_image(url=msg.attachments[0].url)
                else:
                    for attachment in msg.attachments:
                        atch_urls += f"{attachment.url}\n"

            if atch_urls:
                e.add_field(name="Attached Files", value=atch_urls,
                            inline=False)

            try:
                await quote_channel.send(embed=e)
            except Exception as e:
                await ctx.send(f"Error posting to {quote_channel.mention}.")
                raise e
            else:
                num_quoted += 1
                self.bot.dbh.update_quote_count(ctx.guild.id)

        # Could use a pluralization library but one instance is not an issue.
        if num_quoted == 1:
            plural = "message"
        else:
            plural = "messages"

        await ctx.send(f"Quoted {len(msg_ids)} {plural}.")

    @quote.error
    async def quote_error_handler(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("That channel doesn't exist!")
        else:
            raise error

    @quote.command(name='from')
    async def quote_from(self, ctx, channel: discord.TextChannel, *msg_ids):
        """Quote message(s) from a channel other than the current one.

        Args:
            channel (discord.TextChannel): Target channel.
            *msg_ids: Numreic IDs for messages to quote.
        """
        ctx.other_channel = channel
        await ctx.invoke(self.quote, *msg_ids)


def setup(bot):
    bot.add_cog(QuoteCog(bot))
