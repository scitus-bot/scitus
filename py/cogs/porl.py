from random import randint
import requests
import sys

import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get

from pasta import file_to_dict, file_to_list, DATA


data = DATA

helppastas: list = file_to_list(data + "help.txt")
users: dict = file_to_dict(data + "users.json")
roles: dict = file_to_dict(data + "roles.json")



async def handleError(inter: discord.Interaction, error: Exception): # im glad this works
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f}s'.format(error.retry_after)
        await inter.channel.send(msg)
        
    elif isinstance(error, commands.MissingPermissions):
        await inter.send("You cant do that!")
        
    elif isinstance(error, commands.MissingRequiredArgument):
        rnd = randint(0, len(helppastas) - 1)
        msg = helppastas[rnd]
        await inter.channel.send(msg)
        
    else:
        print(error)


#--------------------------------------------------------------------------------------------------------------------------

class Porl(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def is_porl() -> None:
        """ Checks if the current user is me/ninsang/pigeon. """
        def predicate(inter: discord.Interaction) -> bool:
            id: int = inter.user.id
            return id == users["porl"] or id == users["nin"] or id == users["pigeon"]
        return app_commands.check(predicate)

#--------------------------------------------------------------------------------------------------------------------------
    #respawn command (when i inevitably lose all my roles)

    @app_commands.command(
        name="respawn",
        description="Gives me roles (testing).",
    )
    @is_porl()
    async def respawn(self, inter: discord.Interaction) -> None:
        """ Gives the admin roles. """

        roleIds = [
            roles["admin"],
            roles["mod"], 
            roles["porl"],
        ] 

        for roleId in roleIds:
            await inter.user.add_roles(get(inter.guild.roles, id=roleId))

        await inter.response.send_message(
            "https://cdn.discordapp.com/attachments/709182248741503093/856158394292895754/swag.gif"
        )


#--------------------------------------------------------------------------------------------------------------------------
    #removes my roles
    #for testing purposes

    @app_commands.command(
        name="die",
        description="Removes my roles (testing).",
    )
    @is_porl()
    async def die(self, inter: discord.Interaction) -> None:

        roleIds = [
            roles["admin"], 
            roles["mod"], 
            roles["porl"], 
            roles["muted"],
        ]

        for roleId in roleIds:
            await inter.user.remove_roles(get(inter.guild.roles, id=roleId))

        await inter.response.send_message(
            "https://cdn.discordapp.com/emojis/814109742607630397.gif?v=1"
        )


#--------------------------------------------------------------------------------------------------------------------------
    # logout command

    @app_commands.command(
        name="logout",
        description="Logs out the bot.",
    )
    @is_porl()
    async def logout(self, inter: discord.Interaction) -> None:
            
        embed: discord.Embed = discord.Embed(
            title="Success", 
            colour=discord.Colour.green(),
            description=f"Logging out the bot.",
        )
        await inter.response.send_message(embed=embed)
        sys.exit()


#--------------------------------------------------------------------------------------------------------------------------
    # give self

    @app_commands.command(
        name="give_self"
    )
    @is_porl()
    async def give_self(self, inter: discord.Interaction, role: discord.Role) -> None:
        await inter.user.add_roles(role)
        await inter.response.send_message(f"Successfully given: {role.name}")

#--------------------------------------------------------------------------------------------------------------------------
    # host

    @app_commands.command(
        name="hosts",
        description="Lists the public IPs of the hosts of this bot",
    )
    @is_porl()
    async def hosts(self, inter: discord.Interaction, num: int) -> None:
        h = num + "a"
        await inter.response.send_message(
            requests.get("https://ipinfo.io/ip").text,
            ephemeral=True
        )

    @hosts.error
    async def host_error(self, inter: discord.Interaction, error: Exception) -> None:
        await handleError(inter, error)
        
# ----------------------------------------------------------------------------------------------------
    # shutdown
    
    @app_commands.command(
        name="shutdown",
        description="Shuts down the bot"
    )
    @is_porl()
    async def shutdown(self, inter: discord.Interaction) -> None:
        await inter.response.send_message(
            "Quitting...",
            ephemeral=True
        )
        
        sys.exit()
        
    @shutdown.error
    async def shutdown_error(self, inter: discord.Interaction, error: Exception) -> None:
        await handleError(inter, error)


# adds the cog to the main.py and allows it to be used
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Porl(bot))