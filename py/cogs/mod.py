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
    @app_commands.default_permissions(moderate_members=True)
    async def eject(self, inter: discord.Interaction, user: discord.Member, reason: Optional[str] = "") -> None:
        if (user == inter.user) or (user.bot):
            embed: discord.Embed = discord.Embed(title="Invalid user.", colour=0xff0000)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        # muted role
        role = get(inter.guild.roles, id=RoleIDs.mutedRoleID)
        
        # dont mute the user if theyre already muted
        if role in user.roles:
            embed: discord.Embed = discord.Embed(title="User already is muted.", colour=0xff0000)
            await inter.response.send_message(embed=embed, ephemeral=True)
            
        else:
            await user.add_roles(role)
            embed: discord.Embed = discord.Embed(
                title="Success", 
                colour=discord.Colour.green(),
                description=f"**{user.mention}** muted for {reason}.",
            )
            embed.set_footer(text=f"Muted by {inter.user.name}")
            await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    # unmute command
    
    @app_commands.command(
        name="unmute",
        description="Unmutes a user.",
    )
    @app_commands.default_permissions(moderate_members=True)
    async def unmute(self, inter: discord.Interaction, user: discord.Member) -> None:
        if (user == inter.user) or (user.bot):        # prevent self-unmuting
            embed: discord.Embed = discord.Embed(title="Invalid user.", colour=0xff0000)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        # the muted role
        role = get(inter.guild.roles, id=RoleIDs.mutedRoleID)     
        
        # dont unmute the user if theyre not already muted
        if role in user.roles:
            await user.remove_roles(role)
            embed: discord.Embed = discord.Embed(
                title="Success", 
                colour=discord.Colour.green(),
                description=f"**{user.mention}** unmuted.",
            )
            embed.set_footer(text=f"Muted by {inter.user.name}")
            await inter.response.send_message(embed=embed)
            
        else:
            embed: discord.Embed = discord.Embed(title="User is not muted.", colour=0xff0000)
            await inter.response.send_message(embed=embed, ephemeral=True)

    
#--------------------------------------------------------------------------------------------------------------------------
    #@someone

    @app_commands.command(
        name="someone",
        description="Mentions a random user.",
    )
    @app_commands.default_permissions(mention_everyone=True)
    async def someone(self, inter: discord.Interaction) -> None: 

        # getting a list that contains all non-bot members
        members = []
        for m in inter.guild.members:
            if not m.bot:
                members.append(m)
        
        # sending a random one from that list
        rnd = randint(0, len(members) - 1)
        await inter.delete_original_response()
        await inter.channel.send(members[rnd].mention)


#--------------------------------------------------------------------------------------------------------------------------
    #sudo command
    
    @app_commands.command(
        name="sudo",
        description="Sends a message as the bot.",
    )
    @app_commands.default_permissions(mention_everyone=True)
    async def sudo(self, inter: discord.Interaction, message: str) -> None:

        await inter.response.send_message("Done.")
        await inter.channel.send(message)
        await inter.delete_original_response()
    

#--------------------------------------------------------------------------------------------------------------------------
    #kick commands

    @app_commands.command(
        name="kick",
        description="Kicks a user.",
    )
    @app_commands.default_permissions(kick_members=True)
    async def kick(self, inter: discord.Interaction, user: discord.Member, reason: Optional[str] = None) -> None:

        await user.kick(reason=str(reason))
        
        embed: discord.Embed = discord.Embed(
            title="Success", 
            colour=discord.Colour.green(),
            description=f"**{user.mention}** has been kicked for {reason}.",
        )
        embed.set_footer(text=f"Kicked by {inter.user.name}")
        await inter.response.send_message(embed=embed)



#--------------------------------------------------------------------------------------------------------------------------
    #ban command:

    @app_commands.command(
        name="ban",
        description="Bans a user.",
    )
    @app_commands.default_permissions(ban_members=True)
    async def ban(self, inter: discord.Interaction, user: discord.Member, reason: Optional[str] = None) -> None:

        await user.ban(reason=str(reason), delete_message_days=0)
        await user.send(f"You've been banned from {inter.guild.name}\nLLLLLLLLL")
        
        embed: discord.Embed = discord.Embed(
            title="Success", 
            colour=discord.Colour.green(),
            description=f"**{user.mention}** has been banned for {reason}.",
        )
        embed.set_footer(text=f"Banned by {inter.user.name}")
        await inter.response.send_message(embed=embed)
    

#--------------------------------------------------------------------------------------------------------------------------
    #purge

    @app_commands.command(
        name="purge",
        description="Purges an amount of messages.",
    )
    @app_commands.default_permissions(manage_messages=True)
    async def purge(self, inter: discord.Interaction, limit: int) -> None:

        if limit > 50:
            embed: discord.Embed = discord.Embed(title="Too many messages.", colour=0xff0000)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        await inter.channel.purge(limit=(limit+1))
        
        embed: discord.Embed = discord.Embed(
            title="Success", 
            colour=discord.Colour.green(),
            description=f"**{limit}** messages cleared.",
        )
        embed.set_footer(text=f"Purged by {inter.user.name}")
        await inter.channel.send(embed=embed)
        

#--------------------------------------------------------------------------------------------------------------------------
    #nick command
    
    @app_commands.command(
        name="nick",
        description="Changes the nick of a user.",
    )
    @app_commands.default_permissions(manage_nicknames=True)
    async def nick(self, inter: discord.Interaction, user: discord.Member, nick: str) -> None:

        new_user = await user.edit(nick=nick)
        
        embed: discord.Embed = discord.Embed(
            title="Success", 
            colour=discord.Colour.green(),
            description=f"Nickname changed to **{nick}**.",
        )
        embed.set_footer(text=f"Nicked by {inter.user.name}")
        await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    #warn command

    @app_commands.command(
        name="warn",
        description="Warns a user.",
    )
    async def warn(self, inter: discord.Interaction, user: discord.Member, reason: str) -> None:
        if get(inter.guild.roles, id=RoleIDs.modRoleID) not in inter.user.roles:
            embed: discord.Embed = discord.Embed(title="Invalid Permissions.", colour=0xff0000)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        if (user == inter.user) or (user.bot):
            embed: discord.Embed = discord.Embed(title="Invalid User.", colour=0xff0000)
            await inter.response.send_message(embed=embed, ephemeral=True)
            return 
        
        embed: discord.Embed = discord.Embed(
            title="Success", 
            colour=discord.Colour.green(),
            description=f"{user.mention} has been warned.",
        )
        embed.set_footer(text=f"Warned by {inter.user.name}")
        await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    # lockdown 
    
    @app_commands.command(
        name="lockdown",
        description="Locks down a channel",
    )
    @app_commands.default_permissions(manage_channels=True)
    async def lock(self, inter: discord.Interaction) -> None:
        
        await inter.channel.set_permissions(
            inter.guild.default_role, 
            send_messages=False,
            add_reactions=False,
        )
        
        embed: discord.Embed = discord.Embed(
            title="Success",
            colour=discord.Colour.green(),
            description=f"<#{inter.channel.id}> has been locked.",
        )
        embed.set_footer(text=f"Locked by {inter.user.name}")
        await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    # unlockdown.
    
    @app_commands.command(
        name="unlock",
        description="Unlocks a channel",
    )
    @app_commands.default_permissions(manage_channels=True)
    async def unlock(self, inter: discord.Interaction) -> None:
        
        await inter.channel.set_permissions(
            inter.guild.default_role, 
            send_messages=True,
            add_reactions=True,
        )
        
        embed: discord.Embed = discord.Embed(
            title="Success",
            colour=discord.Colour.green(),
            description=f"<#{inter.channel.id}> has been unlocked.",
        )
        embed.set_footer(text=f"Unlocked by {inter.user.name}")
        await inter.response.send_message(embed=embed)
        

#--------------------------------------------------------------------------------------------------------------------------

  
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderator(bot))
