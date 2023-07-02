from random import randint
import requests as rq
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from pasta import ListsPas


async def handleError(message, error):
    """ Handling errors for the command. """
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


def rqget(player: str) -> dict:
    """ Return the dictionary for the players stats in a given gamemode. """
    apirq: rq.Response = rq.get(
        f"https://api.playhive.com/v0/game/all/all/{player}", 
        timeout=30
        )
    return apirq.json()

def gen_display_string(gm: str, data: dict) -> str:
    try:
        sub: dict = data[gm]
        kills, deaths, played, won = sub["kills"], sub["deaths"], sub["played"], sub["victories"]
        
        if deaths == 0: deaths = 1
        if played == 0: played = 1
        
        string: str = (
            f"**{round(kills/deaths, 2)}** ({kills}K {deaths}D)\n" +
            f"**{round(won*100/played, 2)}** ({won}W {played-won}L {played}P)"
        )
    except TypeError:
        string = "**N/A**"
        
    return string

def clean_hive_string(string: str) -> str:
    """ Removes &x from the strings """
    ret_str: list = list(string)
    while "&" in ret_str:
        ind = ret_str.index("&")
        ret_str.pop(ind)
        ret_str.pop(ind)
        
    return "".join(ret_str)

#--------------------------------------------------------------------------------------------------------------------------
class Hive(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._last_member = None

#--------------------------------------------------------------------------------------------------------------------------

    @app_commands.command(
        name="stats",
        description="Stats for the Hive server.",
    )
    async def stats(self, inter: discord.Interaction, player: str) -> None:
        
        await inter.response.send_message("Fetching data....")
        
        data = rqget(player)
        
        emb: discord.Embed = discord.Embed(
            title=f"{data['main']['username']}'s Hive stats",
            description=clean_hive_string(data["main"]["equipped_hub_title"]),
            colour=0xffad14,
        )
        thumb_url = str(data['main']['equipped_avatar']['url'])
        emb.set_thumbnail(url=thumb_url)
        games: list = ["wars", "sg", "sky", "ctf", "bridge"]
        names: list = ["Treasure Wars", "Survival Games", "Sky Wars", "CtF", "Bridge"]
        for i in range(len(games)):
            emb.add_field(
                name=names[i],
                value=gen_display_string(games[i], data),
                inline=True,
            )
        # emb.set_footer(text=f"First played the Hive on <t:{data['main']['first_played']}:D>")
        
        await inter.edit_original_response(
            content="",
            embed=emb,
        )
            
        
        
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Hive(bot))