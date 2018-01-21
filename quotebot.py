import discord
import json
from lib.db_helper import DBHelper
from lib.error_handler_clean import CommandErrorHandler
from discord.ext import commands

# Debugging
print('Loading quotebot...')

# Read our bot token from the configuration file
with open('config.json') as cfg_file:
    # Debugging
    print('Reading configuration file...')

    cfg = json.load(cfg_file)
    token = cfg['token']
    db_file = cfg['db_file']

# Initialize our DB Helper object
dbh = DBHelper(db_file)

# Set up our bot insance
bot = commands.Bot(command_prefix=commands.when_mentioned)


@bot.event
async def on_ready():
    """Actions executed when the bot is logged in and available.
    """
    print('Logged in as {}#{}'.format(bot.user.name, bot.user.discriminator))


@commands.guild_only()
@bot.command()
async def ping(ctx):
    """Simple command to ensure the bot is working.
    """
    await ctx.send('Pong!')


@commands.guild_only()
@bot.command()
async def set_quote_channel(ctx, channel: discord.TextChannel):
    """Set the text channel all quoted messages for a guild are embedded in.

    Args:
        channel (discord.TextChannel): The channel's mention, i.e. #general.
    """
    server_id = ctx.guild.id
    channel_id = channel.id

    if dbh.set_quote_channel(server_id, channel_id):
        await ctx.send('Quote channel for {} is now {}.'
                       .format(ctx.guild.name, channel.mention))
    else:
        await ctx.send('Unable to update channel.')


@commands.guild_only()
@bot.command()
async def stats(ctx):
    """Print some QuoteBot statistics in chat.
    """
    local_qc = dbh.get_quote_count(ctx.guild.id)
    await ctx.send("I've quoted {} messages from {}"
                   .format(local_qc, ctx.guild.name))


# TODO: Take an arbitrary number of msg_id arguments.
@commands.guild_only()
@bot.command()
async def quote(ctx, msg_id: int, channel: discord.TextChannel = None):
    """Quote a message.

    Args:
        msg_id (int): The ID of the message (... > Copy ID)
        channel (discord.TextChannel, optional): Which channel the message is in.
    """
    if channel is None:
        channel = ctx.message.channel

    try:
        msg = await channel.get_message(msg_id)
    except discord.NotFound:
        await ctx.send('No message exists with that ID.')
        return
    except discord.Forbidden:
        await ctx.send('I don\'t have permission to access that channel.')
        return
    except discord.HTTPException as httpe:
        await ctx.send('Got error code {} trying to retrieve message.'
                       .format(httpe.code))
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
        await ctx.send('You haven\'t specified a quote channel!' +
                       'You can set one with `set_quote_channel #channel`.')
        return

    dbh.update_quote_count(ctx.guild.id)

    await quote_channel.send(embed=e)
    await ctx.send('Quoted!')


@quote.error
async def quote_error_handler(ctx, error):
    if isinstance(error, commands.BadArgument):
            await ctx.send('That channel doesn\'t exist!')


# Debugging
print('Adding CommandErrorHandler to bot...')
bot.add_cog(CommandErrorHandler(bot))

# Debugging
print('Starting quotebot...')
bot.run(token)
