import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
from pasta import RoleIDs
import subprocess
import sys

#No "has_role"s


"""
editrole
-colour
-name
-delete
applyall
"""
CDOWN = 20 # cooldown time


#--------------------------------------------------------------------------------------------------------------------------
class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._last_member = None

#--------------------------------------------------------------------------------------------------------------------------
    #colour
    
    @app_commands.command(
        name="editcolour",
        description="Changes the colour of a role.", 
    )
    @app_commands.default_permissions(manage_roles=True)
    async def colour(self, inter: discord.Interaction, role: discord.Role, hex: str) -> None:
        
        clr = discord.Colour(int(hex, base=16))
        await role.edit(colour=clr)
        embed: discord.Embed = discord.Embed(
            title="Success", 
            colour=discord.Colour.green(),
            description=f"**{role.name}**'s colour successfully changed to **{hex}**.",
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    #name
    
    @app_commands.command(
        name="editname",
        description="Changes the name of a role.",
    )
    @app_commands.default_permissions(manage_roles=True)
    async def name(self, inter: discord.Interaction, role: discord.Role, name: str) -> None:
        
        await role.edit(name=name)
        embed: discord.Embed = discord.Embed(
            title="Success", 
            colour=discord.Colour.green(),
            description=f"Role name successfully changed to **{name}**.",
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
        if get(inter.guild.roles, id=RoleIDs.adminRoleID) not in inter.user.roles:
            embed: discord.Embed = discord.Embed(title="Invalid Permissions.", colour=0xff0000)
            await inter.response.send_message(embed=embed)
            return
        
        roleName: str = role.name
        await role.delete()
        embed: discord.Embed = discord.Embed(
            title="Success", 
            colour=discord.Colour.green(),
            description=f"**{roleName}** successfully deleted.",
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
        
        # giving all non-bot users a role
        for member in inter.guild.members:
            if not member.bot:
                await member.add_roles(role)
            else:
                print(f"{member.name} is a bot")
                
                
        embed: discord.Embed = discord.Embed(
            title="Success", 
            colour=discord.Colour.green(),
            description=f"{role.name} successfully given to everyone.",
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    # removeall

    @app_commands.command(
        name="removeall",
        description="Removes a role from every user.",
    )
    @app_commands.default_permissions(administrator=True)
    async def removeall(self, inter: discord.Interaction, role: discord.Role) -> None:
        
        # removing a role from all non-bot users
        for member in inter.guild.members:
            if not member.bot:
                await member.remove_roles(role)
            else:
                print(f"{member.name} is a bot")
        
        embed: discord.Embed = discord.Embed(
            title="Success", 
            colour=discord.Colour.green(),
            description=f"**{role.name}** successfully removed from everyone.",
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
# create role

    @app_commands.command(
        name="createrole",
        description="Creates a role with a given name and colour.",
    )
    @app_commands.default_permissions(manage_roles=True)
    async def createrole(self, inter: discord.Interaction, name: str, hex: str) -> None:
        
        clr = discord.Colour(int(hex, base=16))
        await inter.guild.create_role(name=name, colour=clr)
        embed: discord.Embed = discord.Embed(
            title="Success", 
            colour=discord.Colour.green(),
            description=f"**{name}** successfully created.",
        )
        embed.set_author(name=inter.user.name, icon_url=inter.user.avatar.url)
        await inter.response.send_message(embed=embed)

    
#--------------------------------------------------------------------------------------------------------------------------

    @app_commands.command(
        name="sync",
        description="Syncs the commands up, done sparingly.",
    )
    @app_commands.default_permissions(administrator=True)
    async def sync(self, inter: discord.Interaction) -> None:
        
        await self.bot.tree.sync()
        embed: discord.Embed = discord.Embed(
            title="Syncing complete!", 
            colour=discord.Colour.green(),
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

        await inter.response.send_message("Updating the bot...")


        try:
            subprocess.Popen(["sudo ./update.sh"]) # runs the script saved on the server
            # saves the last commit into a file
            # with open("last_sha.txt", "w") as op:
            #     repo = git.Repo("~/scitus")
            #     sha = repo.head.object.hexsha[:7]
            #     op.write(str(sha))
        except Exception as e:
            await inter.channel.send(f"Error: {e}")
        else:
            sys.exit()  # to prevent any possible clashes 


#--------------------------------------------------------------------------------------------------------------------------

#necessities

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))