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
        # Check to make sure we were given message IDs to quote
        if not msg_ids:
            await ctx.send("Please specify at least one message ID.")
            return

        # quote_channel_id should never be None
        quote_channel_id = self.bot.dbh.get_quote_channel(ctx.guild.id)
        quote_channel = self.bot.get_channel(quote_channel_id)

        # Skip the rest of the function if we don't have a place to put
        # quoted messages.
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
            # If we run into an error processing one message,
            # skip to the next one.
            try:
                msg = await channel.get_message(msg_id)
            except discord.NotFound:
                await ctx.send(f"No message exists with ID {msg_id}.")
                continue
            except discord.Forbidden:
                # TODO: This could spam error messages in the case of
                # quote_from commands. Maybe replace `continue` with `return`.
                await ctx.send(f"I can't access {channel.mention}.")
                continue
            except discord.HTTPException as he:
                await ctx.send(f"Got error code {he.status} " +
                               "trying to retrieve message.")
                continue

            # Users who left the server have no attribute 'color'
            if hasattr(msg.author, 'color'):
                author_color = msg.author.color
            else:
                author_color = discord.Colour(0xFFFFFF)

            # Create our embed object and start adding data to it.
            e = discord.Embed(description=msg.content, color=author_color)
            e.set_author(name=msg.author.display_name,
                         icon_url=msg.author.avatar_url_as(size=128))

            # If the message has more than one attachment (possible via
            # mobile app and bots), simply add the links to the attachments.
            atch_urls = ""
            if msg.attachments:
                if (
                    # If there's only one attachment and it's an image,
                    # attach it to the embed.
                    msg.attachments[0].height and len(msg.attachments) == 1
                ):
                    e.set_image(url=msg.attachments[0].url)
                else:
                    for attachment in msg.attachments:
                        atch_urls += f"{attachment.url}\n"

            # atch_urls is just a string of all the attachment URLs. THey
            # will 404 if the original message is deleted.
            if atch_urls:
                e.add_field(name="Attached Files", value=atch_urls,
                            inline=False)

            try:
                quote_msg = await quote_channel.send(embed=e)
            except discord.Forbidden:
                # To avoid spamming error messages, quit out of the loop if
                # the bot can't access the quote channel.
                await ctx.send(f"Can't post messages to " +
                               "{quote_channel.mention.}. Aborting.")
                return
            except Exception as e:
                await ctx.send(f"Error posting to {quote_channel.mention}.")
                raise e
            else:
                # Increment the statistics count both locally and in the DB.
                num_quoted += 1
                self.bot.dbh.update_quote_count(ctx.guild.id)

            # Try to add all the reactions the original message had.
            # This will fail for reactions from guilds the bot hasn't joined.
            for reaction in msg.reactions:
                try:
                    await quote_msg.add_reaction(reaction)
                except Exception as e:
                    pass

        # Could use a pluralization library but one instance is not an issue.
        if num_quoted == 1:
            plural = "message"
        else:
            plural = "messages"

        await ctx.send(f"Quoted {len(msg_ids)} {plural}.")

    @quote.error
    async def quote_error_handler(self, ctx, error):
        """Error handler for the quote command.

        Args:
            error (TYPE): The error raised by the quote command.
        """
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
