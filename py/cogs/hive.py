"""
kdr (skywars)
"""
import discord
from discord.utils import get
from discord.ext import commands
from discord import app_commands
import requests as rq
from random import randint
from pasta import ListsPas
from typing import Optional


async def handleError(message, error): # im glad this works
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f}s'.format(error.retry_after)
        await message.channel.send(msg)
        
    elif isinstance(error, commands.MissingPermissions):
        await message.send("You cant do that!")
        
    elif isinstance(error, commands.MissingRequiredArgument):
        rnd = randint(0, len(ListsPas.helpPastas) - 1)
        msg = ListsPas.helpPastas[rnd]
        await message.channel.send(msg)
        
    else:
        print(error)


def rqget(gamemode: str, p1: str) -> dict:
    apirq = rq.get(f"https://api.playhive.com/v0/game/all/{gamemode}/{p1}")
    hjs = apirq.json()
    return hjs

def rqget_monthly(gamemode: str, p1: str, year: int, month: int) -> dict:
    apirq = rq.get(f"https://api.playhive.com/v0/game/monthly/player/{gamemode}/{p1}/{year}/{month}")
    hjs = apirq.json()
    return hjs

def stat_string(hive: dict) -> str:
    # sometimes hive doesnt give out the death stat 
    try: deaths = hive["deaths"]
    except: deaths = hive["played"] - hive["victories"]
    kills = hive["kills"]
    wins = hive["victories"]
    played = hive["played"]
    
    statString = f"**{round(kills/deaths, 2)}** ({kills}K {deaths}D)\n**{round(100*wins/played, 2)}%** ({wins}W {played-wins}L {played}P)\n\n"
    
    return statString
    
    
#--------------------------------------------------------------------------------------------------------------------------
class Hive(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._last_member = None



    @app_commands.command(
        name="stats",
        description="Stats for the Hive server.",
    )
    async def stats(self, inter: discord.Interaction, player: str, year: Optional[int] = None, month: Optional[int] = None) -> None:
        
        await inter.response.send_message("Processing....")
        
        if (year or month) and not (year and month):
            embed: discord.Embed = discord.Embed(title="Invalid Arguments.", colour=0xff0000)
            await inter.edit_original_response(embed=embed)
            return
        
        if year and month:
            #treasurewars
            try:
                hjs = rqget_monthly("wars", player, year, month) 

                twstring = stat_string(hjs)
            except:
                twstring = "**N/A**"


            #skywars
            try:
                hjs = rqget_monthly("sky", player, year, month) 

                swstring = stat_string(hjs)
            except:
                swstring = "**N/A**"


            #Survival Games
            try:
                hjs = rqget_monthly("sg", player, year, month) 

                sgstring = stat_string(hjs)
            except:
                sgstring = "**N/A**"
                
            
            # ctf
            try:
                hjs = rqget_monthly("ctf", player, year, month) 

                ctfstring = stat_string(hjs)
            except:
                ctfstring = "**N/A**"
                
        else:
            #treasurewars
            try:
                hjs = rqget("wars", player)

                twstring = stat_string(hjs)
            except:
                twstring = "**N/A**"


            #skywars
            try:
                hjs = rqget("sky", player)

                swstring = stat_string(hjs)
            except:
                swstring = "**N/A**"


            #Survival Games
            try:
                hjs = rqget("sg", player)
                
                sgstring = stat_string(hjs)
            except:
                sgstring = "**N/A**"
                
            
            # ctf
            try:
                hjs = rqget("ctf", player)

                ctfstring = stat_string(hjs)
            except:
                ctfstring = "**N/A**"
        


        # creating the embed
        
        if year and month:
            desc = f"{player}'s Hive stats for {month}/{year}."
        else:
            desc = f"{player}'s Hive stats."
        
        emb: discord.Embed = discord.Embed(title=player, description=desc, colour=discord.Colour(int("ffad14", base=16)))
        emb.set_author(name=inter.user, icon_url=inter.user.display_avatar.url)
        emb.set_thumbnail(url="https://static.wikia.nocookie.net/youtube/images/d/df/HiveGames.jpg/revision/latest?cb=20210726032229")
        emb.add_field(name="Treasure Wars", value=twstring)
        emb.add_field(name="Skywars", value=swstring)
        emb.add_field(name="Survival Games", value=sgstring)
        emb.add_field(name="Capture Flag", value=ctfstring)
        emb.set_footer(text="No Bridge stats yet, and some KDRs may not be 100% accurate.")


        await inter.edit_original_response(content=None, embed=emb)
  


#necesseties
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Hive(bot))