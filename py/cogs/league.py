# going to make a thing that checks the league API for stuff
# idk what stats there are in league bc ive never played it and i have too much
# sex to play league
import requests as rq
import asyncio
from pasta import * # i think its bad coding practise to use import *
from discord.ext import commands # i actually need to install these onto my laptop
# i made this in repl which is why i dont have any of the libraries locally lol


class league(commands.cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def Lstat(self, ctx, player):
        pass
        # ill do it later/tomorrow
