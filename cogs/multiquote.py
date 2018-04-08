import discord
import re
from datetime import datetime
from dateutil import tz
from discord.ext import commands


class MultiQuote():
    def __init__(self, bot):
        self.bot = bot
