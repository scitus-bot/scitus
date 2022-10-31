import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
from pasta import RoleIDs

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
    async def colour(self, inter: discord.Interaction, role: discord.Role, hex: str) -> None:
        # crude check if the user has the necessary role, since its not added in as what it was before
        if get(inter.guild.roles, id=RoleIDs.adminRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return
        
        clr = discord.Colour(int(hex, base=16))
        await role.edit(colour=clr)
        await inter.response.send_message("Role colour changed successfully.")        


#--------------------------------------------------------------------------------------------------------------------------
    #name
    
    @app_commands.command(
        name="editname",
        description="Changes the name of a role.",
    )
    async def name(self, inter: discord.Interaction, role: discord.Role, name: str) -> None:
        if get(inter.guild.roles, id=RoleIDs.adminRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return
        
        await role.edit(name=name)
        await inter.response.send_message("Role name changed successfully.")


#--------------------------------------------------------------------------------------------------------------------------
    # delete role
    
    @app_commands.command(
        name="deleterole",
        description="Deletes a given role.",
    )
    async def delete(self, inter: discord.Interaction, role: discord.Role) -> None:
        if get(inter.guild.roles, id=RoleIDs.adminRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return
        
        roleName: str = role.name
        await role.delete()
        await inter.response.send_message(f"'{roleName}' has been deleted.")


#--------------------------------------------------------------------------------------------------------------------------
  # applyall

    @app_commands.command(
        name="applyall",
        description="Gives a given role to all the members in the server.",
    )
    async def giveall(self, inter: discord.Interaction, role: discord.Role) -> None:
        if get(inter.guild.roles, id=RoleIDs.adminRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return
        
        
        # giving all non-bot users a role
        for member in inter.guild.members:
            if not member.bot:
                await member.add_roles(role)
            else:
                print(f"{member.name} is a bot")
        await inter.response.send_message("Succesfully gave everyone the role.")


#--------------------------------------------------------------------------------------------------------------------------
    # removeall

    @app_commands.command(
        name="removeall",
        description="Removes a role from every user.",
    )
    async def removeall(self, inter: discord.Interaction, role: discord.Role) -> None:
        if get(inter.guild.roles, id=RoleIDs.adminRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return
        
        # removing a role from all non-bot users
        for member in inter.guild.members:
            if not member.bot:
                await member.remove_roles(role)
            else:
                print(f"{member.name} is a bot")
        
        await inter.response.send_message("Succesfully removed the role from everyone.")


#--------------------------------------------------------------------------------------------------------------------------
# create role

    @app_commands.command(
        name="createrole",
        description="Creates a role with a given name and colour.",
    )
    async def createrole(self, inter: discord.Interaction, name: str, hex: str) -> None:
        if get(inter.guild.roles, id=RoleIDs.adminRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return
        
        clr = discord.Colour(int(hex, base=16))
        await inter.guild.create_role(name=name, colour=clr)
        await inter.response.send_message(f"'{name}' role created.")

    
#--------------------------------------------------------------------------------------------------------------------------

    @app_commands.command(
        name="sync",
        description="Syncs the commands up, done sparingly.",
    )
    async def sync(self, inter: discord.Interaction) -> None:
        if get(inter.guild.roles, id=RoleIDs.adminRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return
        
        await self.bot.tree.sync()
        await inter.response.send_message("Syncing complete.")


#--------------------------------------------------------------------------------------------------------------------------

#necessities

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))