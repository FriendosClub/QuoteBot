import discord
import re
from datetime import datetime
from dateutil import tz
from discord.ext import commands


class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # TODO: Make sure this list of extensions is complete.
        self.imgtypes = 'jpg|png|gif|gifv'
        # Embedding videos isn't supported.
        # self.vidtypes = 'mp4|webm'

    def has_img_url(self, msg: str) -> str:
        # TODO: GFYCat support via https://gfycat.com/cajax/get/<id> for URLs
        #       like http://gfycat.com/beautifulunsightlyauklet
        #       (Keep URL but embed "max5mbGif" from API)
        pattern = re.compile(f'https?:\/\/.*?\.({self.imgtypes})',
                             re.IGNORECASE)
        match = pattern.match(msg)

        if not match:
            return None
        else:
            return match.group()

    def utc_to_est(self, msg_timestamp):
        """Converts UTC timestamp to locale’s date and time representation.
        From https://stackoverflow.com/a/4771733/3722806

        Args:
            msg_timestamp (TYPE): UTC timestamp.

        Returns:
            str: String representing locale's date and time representation.
        """
        # Automatically determine time zones.
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        # Convert UTC message timestamp to local time.
        utc = msg_timestamp.replace(tzinfo=from_zone)

        # Return timezone string in local time.
        return utc.astimezone(to_zone).strftime('%b. %d, %Y, %I:%M %p')

    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def quote(self, ctx, *msg_ids):
        """Quotes a message.

        Args:
            *msg_ids: Numeric IDs for messages to quote
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

        msg_id = msg_ids[0]
        # If we're quoting a lot of messages, it'll take a while before
        # confirmation is posted. Trigger typing in the meantime.
        await ctx.channel.trigger_typing()
        # We'll get a 403 error that kills everything else if this
        # runs into any issues, so just pass over any exceptions and let
        # the rest of our error handling take care of the problem.
        try:
            await quote_channel.trigger_typing()
        except Exception as e:
            pass

        # If we run into an error processing one message,
        # skip to the next one.
        try:
            if msg_id.isnumeric():
                msg = await channel.fetch_message(msg_id)
                message = msg.content
                user = self.bot.get_user(msg.author.id)
            else:
                message = msg_id
                user_id = int("".join(filter(str.isdigit, msg_ids[1])))
                user = self.bot.get_user(user_id)
        except discord.NotFound:
            await ctx.send(f"No message exists with ID `{msg_id}`.")
        except discord.Forbidden:
            # Break out of the quote loop if we can't access the quote
            # channel.
            await ctx.send(f"I can't access {channel.mention}.")
            return
        except discord.HTTPException as he:
            await ctx.send(f"Got error code `{he.status}` " +
                           "trying to retrieve message.")
            raise he

        # Users who left the server have no attribute 'color'
        if hasattr(user, 'color'):
            author_color = user.color
        else:
            author_color = discord.Colour(0xFFFFFF)

        # Create our embed object and start adding data to it.
        e = discord.Embed(description=message, color=author_color)
        e.set_author(name=user.display_name,
                     icon_url=user.avatar_url_as(size=128))

        # If the message has more than one attachment (possible via
        # mobile app and bots), simply add the links to the attachments.
        if msg_id.isnumeric():
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
            # If there's no attachments, check for links we can embed
            else:
                pic = self.has_img_url(message)
    
                if pic and not e.image.url:
                    e.set_image(url=pic)
    
    
            # atch_urls is just a string of all the attachment URLs. THey
            # will 404 if the original message is deleted.
            if atch_urls:
                e.add_field(name="Attached Files", value=atch_urls,
                            inline=False)
                            
            # Fill out footer info: Date and text channel
            # TODO: Add message ID?
            e.set_footer(text=f"{self.utc_to_est(msg.created_at)}")
        else:
            # Fill out footer info: Date and text channel
            # TODO: Add message ID?
            e.set_footer(text=f"{datetime.now().strftime('%b. %d, %Y, %I:%M %p')}")

        try:
            quote_msg = await quote_channel.send(embed=e)
        except discord.Forbidden:
            # To avoid spamming error messages, quit out of the loop if
            # the bot can't access the quote channel.
            await ctx.send("Can't post messages to " +
                           f"{quote_channel.mention}. Aborting.")
            return
        except Exception as e:
            await ctx.send(f"Error posting to {quote_channel.mention}.")
            raise e
        else:
            # Increment the statistics count both locally and in the DB.
            # TODO: Figure out why this gets incremented despite having
            #       continue statement theoretically skip this logic.
            num_quoted += 1
            self.bot.dbh.update_quote_count(ctx.guild.id)

        if msg_id.isnumeric():
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
            
        await ctx.message.delete()

    @quote.error
    async def quote_error_handler(self, ctx, error):
        """Error handler for the quote command.

        Args:
            error: The error raised by the quote command.
        """
        if isinstance(error, commands.BadArgument):
            await ctx.send("That channel doesn't exist!")
        else:
            print("Encountered error in quote comand:")
            raise error

    @quote.command(name='from')
    async def quote_from(self, ctx, channel: discord.TextChannel, *msg_ids):
        """Quote message(s) from a channel other than the current one.

        Args:
            channel (discord.TextChannel): Target channel.
            *msg_ids: Numeric IDs for messages to quote.
        """
        ctx.other_channel = channel
        await ctx.invoke(self.quote, *msg_ids)


def setup(bot):
    bot.add_cog(Quote(bot))
