"""
List of commands:
  -Silence
  -Free
  -Sudo
  -Someone 
  -purge
  -nick
"""


import discord
from discord.utils import get
from discord.ext import commands
from discord import app_commands
from random import randint
from pasta import ListsPas, RoleIDs, UserIDs
from typing import Optional


# im going to use this function as a general error handling thing
async def handleError(message, error): 
    """ Multi-use error handler """
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f}s'.format(error.retry_after)
        await message.channel.send(msg)
        
    elif isinstance(error, commands.MissingPermissions):
        await message.channel.send("You cant do that!")
        
    elif isinstance(error, commands.MissingRole):
        await message.channel.send("You cant do that!")
        
    elif isinstance(error, commands.MissingRequiredArgument):
        rnd = randint(0, len(ListsPas.helpPastas) - 1)
        msg = ListsPas.helpPastas[rnd]
        await message.channel.send(msg)
        
    else:
        print(error)


#--------------------------------------------------------------------------------------------------------------------------
class Moderator(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


#--------------------------------------------------------------------------------------------------------------------------
    #mute command
    
    @app_commands.command(
        name="mute",
        description="Mutes a user.",
    )
    async def eject(self, inter: discord.Interaction, user: discord.Member, time: Optional[str] = None) -> None:
        if get(inter.guild.roles, id=RoleIDs.modRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return
        
        if (user == inter.user) or (user.bot):
            await inter.response.send_message("Invalid user.")
            return
        
        
        role = get(inter.guild.roles, id=RoleIDs.mutedRoleID)
        if role in user.roles:
            await inter.response.send_message("This person is already ejected.")
        else:
            await user.add_roles(role)
            await inter.response.send_message(f"{user} was the imposter.")


#--------------------------------------------------------------------------------------------------------------------------
    # unmute command
    
    @app_commands.command(
        name="unmute",
        description="Unmutes a user.",
    )
    async def unmute(self, inter: discord.Interaction, user: discord.Member) -> None:
        if get(inter.guild.roles, id=RoleIDs.modRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return

        if (user == inter.user) or (user.bot):        # prevent self-unmuting
            await inter.response.send_message("You cannot unmute yourself.")
            return
        

        role = get(inter.guild.roles, id=RoleIDs.mutedRoleID)     # the muted role
        if role in user.roles:
            await user.remove_roles(role)
            await inter.response.send_message(f"{user} you have been freed.")
        else:
            await inter.response.send_message("This user is not muted.")

    
#--------------------------------------------------------------------------------------------------------------------------
    #@someone

    @app_commands.command(
        name="someone",
        description="Mentions a random user.",
    )
    async def someone(self, inter: discord.Interaction) -> None: 
        if get(inter.guild.roles, id=RoleIDs.modRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return
        
        # getting a list that contains all non-bot members
        members = []
        for m in inter.guild.members:
            if not m.bot:
                members.append(m)
        

        rnd = randint(0, len(members) - 1)
        await inter.delete_original_response()
        await inter.channel.send(members[rnd].mention)


#--------------------------------------------------------------------------------------------------------------------------
    #sudo command
    
    @app_commands.command(
        name="sudo",
        description="Sends a message as the bot.",
    )
    async def sudo(self, inter: discord.Interaction, message: str) -> None:
        if get(inter.guild.roles, id=RoleIDs.modRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return

        await inter.channel.send(message)
        await inter.delete_original_response()
    

#--------------------------------------------------------------------------------------------------------------------------
    #kick commands

    @app_commands.command(
        name="kick",
        description="Kicks a user.",
    )
    async def kick(self, inter: discord.Interaction, user: discord.Member, reason: Optional[str] = None) -> None:
        if get(inter.guild.roles, id=RoleIDs.modRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return


        await user.kick(reason=str(reason))

        await inter.response.send_message(f"{user.mention} has been kindly removed by {inter.user.mention} <:wholesome:806907457342930975> \n Reason: {str(reason)}")


#--------------------------------------------------------------------------------------------------------------------------
    #ban command:

    @app_commands.command(
        name="ban",
        description="Bans a user.",
    )
    async def ban(self, inter: discord.Interaction, user: discord.Member, reason: Optional[str] = None) -> None:
        if get(inter.guild.roles, id=RoleIDs.modRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return

        await user.ban(reason=str(reason), delete_message_days=0)
        await user.send(f"You've been banned from {inter.guild.name}\nLLLLLLLLL")
        await inter.response.send_message(f"{user.mention} has left. {inter.user.mention} <:peepoSad:809355473831854132> \n Reason: {str(reason)}")
    

#--------------------------------------------------------------------------------------------------------------------------
    #purge

    @app_commands.command(
        name="purge",
        description="Purges an amount of messages.",
    )
    async def purge(self, inter: discord.Interaction, limit: int) -> None:
        if get(inter.guild.roles, id=RoleIDs.modRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return

        if limit > 50:
            await inter.response.send_message("Purge less messages dipshit")
            return

        await inter.channel.purge(limit=(limit+1))
        await inter.response.send_message(f"{limit} messages cleared.")
        

#--------------------------------------------------------------------------------------------------------------------------
    #nick command
    
    @app_commands.command(
        name="nick",
        description="Changes the nick of a user.",
    )
    async def nick(self, inter: discord.Interaction, user: discord.Member, nick: str) -> None:
        if get(inter.guild.roles, id=RoleIDs.modRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return

        new_user = await user.edit(nick=nick)
        await inter.response.send_message("Nickname changed.")


#--------------------------------------------------------------------------------------------------------------------------
    #warn command

    @app_commands.command(
        name="warn",
        description="Warns a user.",
    )
    async def warn(self, inter: discord.Interaction, user: discord.Member, reason: str) -> None:
        if get(inter.guild.roles, id=RoleIDs.modRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return
        
        if (user == inter.user) or (user.bot):
            await inter.response.send_message("Invalid user.")
            return 
        
        await inter.response.send_message(f"{user.mention} has been warned.")


#--------------------------------------------------------------------------------------------------------------------------
    # lockdown 
    
    @app_commands.command(
        name="lockdown",
        description="Locks down a channel",
    )
    async def lock(self, inter: discord.Interaction) -> None:
        if get(inter.guild.roles, id=RoleIDs.modRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return
        
        await inter.channel.set_permissions(
            inter.guild.default_role, 
            send_messages=False,
            add_reactions=False,
            )
        await inter.response.send_message("Channel locked 👍")


#--------------------------------------------------------------------------------------------------------------------------
    # unlockdown
    
    @app_commands.command(
        name="unlock",
        description="Unlocks a channel",
    )
    async def unlock(self, inter: discord.Interaction) -> None:
        if get(inter.guild.roles, id=RoleIDs.modRoleID) not in inter.user.roles:
            await inter.response.send_message("Invalid permissions.")
            return
        
        await inter.channel.set_permissions(
            inter.guild.default_role, 
            send_messages=True,
            add_reactions=True,
            )
        await inter.response.send_message("Channel unlocked 👍")
        

#--------------------------------------------------------------------------------------------------------------------------

  
# this bit is just necessary i should probably look into why
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderator(bot))
