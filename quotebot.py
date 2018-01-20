import discord
import json
import sqlite3
from discord.ext import commands

with open('config.json') as cfg_file:
    cfg = json.load(cfg_file)
    token = cfg['token']

# TODO: Implement a DB so we can support multiple servers
quote_channel_id = 404041101805223936

bot = commands.Bot(command_prefix=commands.when_mentioned)


@bot.event
async def on_ready():
    print('Logged in as {}#{}'.format(bot.user.name, bot.user.discriminator))


@commands.guild_only()
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


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


# TODO: Move this to a config file
bot.run(token)
