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

# Set up our bot insance
bot = commands.Bot(command_prefix=commands.when_mentioned)

# Initialize our DB Helper object
bot.dbh = DBHelper(db_file)


@bot.event
async def on_ready():
    """Actions executed when the bot is logged in and available.
    """
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}")


if __name__ == '__main__':
    # Load all our cogs, then run the bot
    print("Loading extensions...")
    extensions = ['cogs.error_handler',
                  'cogs.ping',
                  'cogs.stats',
                  'cogs.guild_config',
                  'cogs.quote']
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}")


print("Starting quotebot...")
bot.run(token, reconnect=True)
