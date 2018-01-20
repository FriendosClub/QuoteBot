import discord
import json
import sqlite3
from discord.ext import commands

# Read our bot token from the configuration file
with open('config.json') as cfg_file:
    cfg = json.load(cfg_file)
    token = cfg['token']
    db_file = cfg['db_file']

# Set up our bot insance
bot = commands.Bot(command_prefix=commands.when_mentioned)


def db_init():
    """Initializes the table(s) in the DB
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS guilds
                   (guild_id INTEGER NOT NULL UNIQUE,
                    quote_channel INTEGER NOT NULL,
                    quote_count INTEGER NOT NULL DEFAULT 0 CHECK(quote_count >= 0),
                    PRIMARY KEY guild_id)''')
    conn.commit()
    conn.close()


def db_get_quote_channel(guild_id: int) -> int:
    """Retrieve the ID of the channel for posting quotes

    Args:
        guild_id (int): ID of the specific guild

    Returns:
        int: The quote channel ID
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('SELECT quote_channel FROM guilds WHERE id=?', (guild_id,))
    # Guild IDs/entries are unique, so there will only be zero or one results.
    result = cursor.fetchone()

    conn.close()

    if not result:
        return None
    else:
        # Return the only item in the tuple
        return result[0]


def db_set_quote_channel(guild_id: int, channel_id: int) -> bool:
    """Inserts or updates the required information for a guild.

    Args:
        guild_id (int): The ID of the guild
        channel_id (int): The ID of the quote channel

    Returns:
        bool: True if the insert/update succeeded.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    result = False

    q = '''INSERT OR REPLACE INTO guilds (guild_id, quote_channel, quote_count)
           VALUES (?, ?, (SELECT quote_count FROM guilds WHERE guild_id=?))'''

    # TODO: Implement error handling for this query (CHECK fail, etc.)
    cursor.execute(q, (guild_id, channel_id, guild_id))
    result = True

    conn.commit()
    conn.close()
    return result


@bot.event
async def on_ready():
    print('Logged in as {}#{}'.format(bot.user.name, bot.user.discriminator))


@commands.guild_only()
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


@commands.guild_only()
@bot.command()
async def set_quote_channel(ctx, channel: discord.TextChannel):
    server_id = ctx.guild.id
    channel_id = channel.id

    if db_set_quote_channel(server_id, channel_id):
        await ctx.send('Quote channel for {} is now {}.'
                       .format(ctx.guild.name, channel.mention))
    else:
        await ctx.send('Unable to update channel.')


# TODO: Take an arbitrary number of msg_id arguments.
@commands.guild_only()
@bot.command()
async def quote(ctx, channel: discord.TextChannel, msg_id: int):
    if channel is None:
        await ctx.send('A channel with that name doesn\'t exist!')
        return

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

    quote_channel = bot.get_channel(quote_channel_id)
    await quote_channel.send(embed=e)
    await ctx.send('Quoted!')


db_init()
bot.run(token)
