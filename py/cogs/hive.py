import discord
from discord.utils import get
from discord.ext import commands
import asyncio
import random
from pasta import *
import requests as rq



"""
kdr (skywars)
"""
def rqget(gamemode, p1):
        apirq = rq.get("https://api.playhive.com/v0/game/all/{}/{}".format(gamemode, p1))
        hjs = apirq.json()
        return hjs

async def handleError(error, ctx):
  if isinstance(error, commands.CommandOnCooldown):
    msg = 'This command is on cooldown, please try again in {:.2f}s'.format(error.retry_after)
    await ctx.channel.send(msg)
  else:
    raise error



#--------------------------------------------------------------------------------------------------------------------------
class hive(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None



  @commands.command(
    help="Outputs your stats for 3 Hive Games."
  )
  @commands.cooldown(1, 5, commands.BucketType.guild)
  async def stats(self, ctx, player):
        #treasurewars
    hjs = rqget("wars", player) #the hivejson im using updates each time this function is used

    twk, twd, tww, twl, twp = hjs["kills"], hjs["deaths"], hjs["victories"], hjs["played"] - hjs["victories"], hjs["played"]
    twkdr, twwlr = round(twk/twd, 2), round(tww/twl, 2)

    #annoying big string
    twstring = f"Treasure Wars:\n{twkdr} ({twk}K {twd}D)\n{twwlr} ({tww}W {twl}L {twp}P)\n\n"



    #skywars
    hjs = rqget("sky", player)

    swk, swd, sww, swp = hjs["kills"], hjs["played"] - hjs["victories"], hjs["victories"], hjs["played"]
    swkdr, swwlr = round(swk/swd, 2), round(sww/swd, 2)

    #annoying big string p2
    swstring = f"Skywars:\n{swkdr} ({swk}K {swd}D)\n{swwlr} ({sww}W {swd}L {swp}P)\n\n"



    #Survival Games
    hjs = rqget("sg", player)

    sgk, sgd, sgw, sgp = hjs["kills"], hjs["played"] - hjs["victories"], hjs["victories"], hjs["played"]
    sgkdr, sgwlr = round(sgk/sgd, 2), round(sgw/sgd, 2)
    
    #annoying big string p3
    sgstring = f"Survival Games:\n{sgkdr} ({sgk}K {sgd}D)\n{sgwlr} ({sgw}W {sgd}L {sgp}P)"



    #annoying big string: finale
    superstring = twstring + swstring + sgstring

    await ctx.channel.send(superstring)
  

  @stats.error
  async def stats_error(self, ctx, error):
    await handleError(error, ctx)

#necesseties
def setup(bot):
  bot.add_cog(hive(bot))