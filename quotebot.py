import discord
import json
from lib.db_helper import DBHelper
from discord.ext import commands

print("Loading quotebot...")

# Read our bot token from the configuration file
with open('config.json') as cfg_file:
    print("Reading configuration file...")

    cfg = json.load(cfg_file)

# Set up our bot insance
bot = commands.Bot(command_prefix=commands.when_mentioned,
                   owner_id=cfg['owner_id'])

# Initialize our DB Helper object
bot.dbh = DBHelper(cfg['db_file'])


@bot.event
async def on_ready():
    """Actions executed when the bot is logged in and available.
    """
    print(f"Logged in as {bot.user.name}#{bot.user.discriminator}")


if __name__ == '__main__':
    # Load all our cogs, then run the bot
    print("Loading extensions...")
    bot.ext_names = ['cogs.ping',
                     'cogs.stats',
                     'cogs.guild_config',
                     'cogs.quote',
                     'cogs.reload_extension']
    for extension in bot.ext_names:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"> Failed to load extension {extension}")
            raise e
        else:
            print(f"> Loaded {extension[5:]}")


print("Starting quotebot...")
bot.run(cfg['token'], reconnect=True)
