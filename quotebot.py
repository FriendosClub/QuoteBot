# TODO:
#  - Implement `unquote` command
#  - Update `stats` command to include global stats
#  - Implement a `create_quote_channel` command
#  - Look into using an actual database rather than sqlite
#  - More testing!!!

import discord
import json
from lib.db_helper import DBHelper
from discord.ext import commands

print("Loading quotebot...")

# Read our bot token from the configuration file
with open('config.json') as cfg_file:
    print("Reading configuration file...")

    cfg = json.load(cfg_file)
    token = cfg['token']
    db_file = cfg['db_file']

# Initialize our DB Helper object
dbh = DBHelper(db_file)

# Set up our bot insance
bot = commands.Bot(command_prefix=commands.when_mentioned)


# TODO: Error handler for incorrect channel
@commands.guild_only()
@commands.has_permissions(administrator=True)
@bot.command()
async def set_quote_channel(ctx, channel: discord.TextChannel):
    """Set the text channel all quoted messages for a guild are embedded in.

    Args:
        channel (discord.TextChannel): The channel's mention, i.e. #general.
    """
    server_id = ctx.guild.id
    channel_id = channel.id

    if dbh.set_quote_channel(server_id, channel_id):
        await ctx.send(f"Quote channel for {ctx.guild.name} is now {channel.mention}.")
    else:
        await ctx.send("Unable to update channel.")


@commands.guild_only()
@bot.command()
async def stats(ctx):
    """Print some QuoteBot statistics in chat.
    """
    local_qc = dbh.get_quote_count(ctx.guild.id)
    await ctx.send(f"I've quoted {local_qc} messages from {ctx.guild.name}")


# TODO: Take an arbitrary number of msg_id arguments.
@commands.guild_only()
@bot.command()
async def quote(ctx, msg_id: int, channel: discord.TextChannel = None):
    """Quote a message.

    Args:
        msg_id (int): The ID of the message (... > Copy ID)
        channel (discord.TextChannel, optional): Which channel to search.
    """
    if channel is None:
        channel = ctx.message.channel

    try:
        msg = await channel.get_message(msg_id)
    except discord.NotFound:
        await ctx.send("No message exists with that ID.")
        return
    except discord.Forbidden:
        await ctx.send("I don't have permission to access that channel.")
        return
    except discord.HTTPException as he:
        await ctx.send(f"Got error code {he.code} trying to retrieve message.")
        return

    e = discord.Embed(description=msg.content, color=msg.author.color)
    e.set_author(name=msg.author.display_name,
                 icon_url=msg.author.avatar_url_as(size=64))

    # TODO: Handle up to 10 possible attachments
    # TODO: Handle attachments that aren't images
    if msg.attachments and hasattr(msg.attachments[0], 'height'):
        e.set_image(url=msg.attachments[0].url)

    quote_channel_id = dbh.get_quote_channel(ctx.guild.id)
    quote_channel = bot.get_channel(quote_channel_id)

    if quote_channel is None:
        await ctx.send("You haven't specified a quote channel! " +
                       "You can set one with `set_quote_channel #channel`.")
        return

    dbh.update_quote_count(ctx.guild.id)

    await quote_channel.send(embed=e)
    await ctx.send("Quoted!")


@quote.error
async def quote_error_handler(ctx, error):
    if isinstance(error, commands.BadArgument):
            await ctx.send("That channel doesn't exist!")


@bot.event
async def on_ready():
    """Actions executed when the bot is logged in and available.
    """
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}")


if __name__ == '__main__':
    # Load all our cogs, then run the bot
    print("Loading extensions...")
    extensions = ['cogs.error_handler', 'cogs.ping']
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}")


print("Starting quotebot...")
bot.run(token, reconnect=True)
