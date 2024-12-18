from typing import Optional
import sys
import subprocess

import discord
from discord import app_commands
from discord.ext import commands
from git import Repo

import json
from pasta import success_embed, fail_embed

CDOWN = 20 # cooldown time


#--------------------------------------------------------------------------------------------------------------------------
class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._last_member = None

#--------------------------------------------------------------------------------------------------------------------------
    # change role colour
    
    @app_commands.command(
        name="editcolour",
        description="Changes the colour of a role.", 
    )
    @app_commands.default_permissions(manage_roles=True)
    async def colour(self, inter: discord.Interaction, role: discord.Role, hex: str) -> None:
        """ Changes the colour of a specified role. """

        clr = discord.Colour(int(hex, base=16))
        await role.edit(colour=clr)

        embed: discord.Embed = success_embed(
            f"**{role.name}**'s colour successfully changed to **{hex}**."
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    # change role name

    @app_commands.command(
        name="editname",
        description="Changes the name of a role.",
    )
    @app_commands.default_permissions(manage_roles=True)
    async def name(self, inter: discord.Interaction, role: discord.Role, name: str) -> None:
        """ Changes the name of a specified role. """

        await role.edit(name=name)

        embed: discord.Embed = success_embed(
            f"Role name successfully changed to **{name}**."
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    # delete role

    @app_commands.command(
        name="deleterole",
        description="Deletes a given role.",
    )
    @app_commands.default_permissions(manage_roles=True)
    async def delete(self, inter: discord.Interaction, role: discord.Role) -> None:
        """ Deletes a specified role. """

        role_name: str = role.name
        await role.delete()

        embed: discord.Embed = success_embed(
            f"**{role_name}** successfully deleted."
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    # applyall

    @app_commands.command(
        name="applyall",
        description="Gives a given role to all the members in the server.",
    )
    @app_commands.default_permissions(administrator=True)
    async def giveall(self, inter: discord.Interaction, role: discord.Role) -> None:
        """ Give all members a specified role. """

        # placeholder response
        await inter.response.send_message("Working...")

        # giving all non-bot users a role
        for member in inter.guild.members:
            if not member.bot:
                await member.add_roles(role)
            else:
                print(f"{member.name} is a bot")


        embed: discord.Embed = success_embed(
            f"{role.name} successfully given to everyone."
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.edit_original_response(content=None, embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    # removeall

    @app_commands.command(
        name="removeall",
        description="Removes a role from every user.",
    )
    @app_commands.default_permissions(administrator=True)
    async def removeall(self, inter: discord.Interaction, role: discord.Role) -> None:
        """ Remove from all members a specified role. """

        # placeholder reply
        await inter.response.send_message("Working...")

        # removing a role from all non-bot users
        for member in inter.guild.members:
            if not member.bot:
                await member.remove_roles(role)
            else:
                print(f"{member.name} is a bot")


        embed: discord.Embed = success_embed(
            f"**{role.name}** successfully removed from everyone."
            )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.edit_original_response(content=None, embed=embed)



#--------------------------------------------------------------------------------------------------------------------------
    # create role

    @app_commands.command(
        name="createrole",
        description="Creates a role with a given name and colour.",
    )
    @app_commands.default_permissions(manage_roles=True)
    async def createrole(self, inter: discord.Interaction, name: str, hex: str) -> None:
        """ Creates a new role. """

        clr = discord.Colour(int(hex, base=16))
        await inter.guild.create_role(name=name, colour=clr)

        embed: discord.Embed = success_embed(
            f"**{name}** successfully created."
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.response.send_message(embed=embed)

    
#--------------------------------------------------------------------------------------------------------------------------
    # sync commands

    @app_commands.command(
        name="sync",
        description="Syncs the commands up, done sparingly.",
    )
    @app_commands.default_permissions(administrator=True)
    async def sync(self, inter: discord.Interaction) -> None:
        """ Syncs commands with the API (???). """

        await self.bot.tree.sync()

        embed: discord.Embed = success_embed(
            "Syncing complete."
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    # update command # real

    @app_commands.command(
        name="update",
        description="Updates the bot to the latest version on github",
    )
    @app_commands.default_permissions(administrator=True)
    async def update(self, inter: discord.Interaction) -> None:
        """ Updating the bot on the Raspberry Pi. """

        await inter.response.send_message("Updating the bot...", ephemeral=True)

        # want to try and prevent it from deleting itself 
        # if there is an obvious error in the code that will 
        # prevent it from running

        try:
            subprocess.Popen(["./update.sh"])   # runs the script saved on the server
            sys.exit()  # to prevent any possible clashes 
        except Exception as e:
            await inter.channel.send(f"Error: {e}")


#--------------------------------------------------------------------------------------------------------------------------
    # version

    @app_commands.command(
        name="version",
        description="Gets the last short commit hash that the bot is running on.",
    )
    async def version(self, inter: discord.Interaction) -> None:
        """ Gets the last short hash of the commit """
        
        rep: Repo = Repo("scitus/")
        
        embed: discord.Embed = discord.Embed(
            title=f"Version: {str(rep.head.commit)[:7]}", 
            colour=discord.Colour.green(),
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.response.send_message(embed=embed)



#--------------------------------------------------------------------------------------------------------------------------
    # sync all channels in category 

    @app_commands.command(
        name="sync_channels",
        description="Syncs channel permissions to the channel category",
    )
    @app_commands.default_permissions(administrator=True)
    async def sync_channels(self, inter: discord.Interaction, category: discord.CategoryChannel) -> None:
        """ Syncs """

        await inter.response.send_message("Syncing ... ")

        for channel in category.channels:
            await channel.edit(sync_permissions=True)

        embed: discord.Embed = success_embed(
            "Syncing complete!"
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.edit_original_response(content=None, embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    # update the jojo timestamp
    
    @app_commands.command(
        name="jojo_update",
        description="Updated the JoJo countdown timer to the given timestamp"
    )
    @app_commands.default_permissions(administrator=True)
    async def jojo_update(
            self, 
            inter: discord.Interaction, 
            time: Optional[int], 
            event: Optional[str]
        ) -> None:
        """ Updates the countdown timer """

        await inter.response.send_message("Changing....")

        if len(event) > 16:
            embed: discord.Embed = fail_embed("Event name too long!")
            embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
            await inter.edit_original_response(content=None, embed=embed)
            
            return
        
        countdown: dict = {
            "timestamp": time,
            "event": event
        }
        
        data = r"C:\Users\nathan\code\discord\scitus\data" + "\\"
        
        with open(data + "jojo.json", "w") as file:
            json.dump(countdown, file)
            
        embed: discord.Embed = success_embed("Successfully changed")
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.edit_original_response(content=None, embed=embed)

        
        
        


#--------------------------------------------------------------------------------------------------------------------------
#necessities

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))
