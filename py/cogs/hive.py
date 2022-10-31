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

#--------------------------------------------------------------------------------------------------------------------------
class Hive(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._last_member = None



    @app_commands.command(
        name="stats",
        description="Stats for the Hive server.",
    )
    async def stats(self, inter: discord.Interaction, player: str) -> None:
        
        await inter.response.send_message("Processing....")
        
        #treasurewars
        hjs = rqget("wars", player) #the hivejson im using updates each time this function is used

        twk, twd, tww, twl, twp = hjs["kills"], hjs["deaths"], hjs["victories"], hjs["played"] - hjs["victories"], hjs["played"]
        twkdr, twwlr = round(twk/twd, 2), round(tww/twl, 2)

        #annoying big string
        twstring = f"**{twkdr}** ({twk}K {twd}D)\n**{twwlr}** ({tww}W {twl}L {twp}P)\n\n"



        #skywars
        hjs = rqget("sky", player)

        swk, swd, sww, swp = hjs["kills"], hjs["played"] - hjs["victories"], hjs["victories"], hjs["played"]
        swkdr, swwlr = round(swk/swd, 2), round(sww/swd, 2)

        #annoying big string p2
        swstring = f"**{swkdr}** ({swk}K {swd}D)\n**{swwlr}** ({sww}W {swd}L {swp}P)\n\n"



        #Survival Games
        hjs = rqget("sg", player)

        sgk, sgd, sgw, sgp = hjs["kills"], hjs["played"] - hjs["victories"], hjs["victories"], hjs["played"]
        sgkdr, sgwlr = round(sgk/sgd, 2), round(sgw/sgd, 2)

        #annoying big string p3
        sgstring = f"**{sgkdr}** ({sgk}K {sgd}D)\n**{sgwlr}** ({sgw}W {sgd}L {sgp}P)"


        # creating the embed
        emb: discord.Embed = discord.Embed(title=player, description=f"{player}'s Hive Stats.", colour=discord.Colour(int("ffad14", base=16)))
        emb.set_author(name=inter.user, icon_url=inter.user.display_avatar.url)
        emb.set_thumbnail(url="https://static.wikia.nocookie.net/youtube/images/d/df/HiveGames.jpg/revision/latest?cb=20210726032229")
        emb.add_field(name="Treasure Wars", value=twstring)
        emb.add_field(name="Skywars", value=swstring)
        emb.add_field(name="Survival Games", value=sgstring)


        await inter.followup.send(embed=emb)
  


#necesseties
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Hive(bot))