#!/usr/bin/env python3

import discord
import json
from quotebot.database import DBHelper
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
    print(f"> Connected to {len(bot.guilds)} guilds")

    total_members = 0
    for guild in bot.guilds:
        for member in guild.members:
            total_members += 1

    print(f"> Serving {total_members} members")


if __name__ == '__main__':
    # Load all our cogs, then run the bot
    print("Loading extensions...")
    bot.ext_names = [
        'ping',
        'stats',
        'guild_config',
        'quote',
        'unquote',
        'reload',
        'invite',
    ]
    for extension in bot.ext_names:
        ext_name = f'quotebot.cogs.{extension}'
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"> Failed to load extension {extension}")
            raise e
        else:
            print(f"> Loaded {extension[5:]}")

    print("Starting quotebot...")
    bot.run(cfg['token'], reconnect=True)
