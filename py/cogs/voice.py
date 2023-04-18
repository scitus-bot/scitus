from asyncio import sleep

import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get

# this does not work 

class Voice(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._last_member = None


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Voice(bot))