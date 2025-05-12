from random import randint
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get

from pasta import success_embed, fail_embed, file_to_dict, DATA

data = DATA

roles: dict = file_to_dict(data + "roles.json")
users: dict = file_to_dict(data + "users.json")


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
    async def eject(
            self, inter: discord.Interaction,
            user: discord.Member, reason: Optional[str] = "") -> None:
        """ Mutes a user """
        
        # cannot mute yourself or a bot account
        if user == inter.user or user.bot:
            embed: discord.Embed = fail_embed("Invalid user.")
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        # muted role
        role = get(inter.guild.roles, id=roles["muted"])
        
        # dont mute the user if theyre already muted
        if role in user.roles:
            embed: discord.Embed = fail_embed("User is already muted.")
            await inter.response.send_message(embed=embed, ephemeral=True)
            return 
        
        # muting the user
        await user.add_roles(role)
        
        embed: discord.Embed = success_embed(
            f"**{user.mention}** muted for {reason}."
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
    async def unmute(self, inter: discord.Interaction,
                     user: discord.Member) -> None:
        """ Unmutes a user """
        
        if user == inter.user or user.bot:  # prevent self-unmuting
            embed: discord.Embed = fail_embed("Invalid user.")
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        # the muted role
        role = get(inter.guild.roles, id=roles["muted"])     
        
        # dont unmute the user if theyre not already muted
        if role not in user.roles:
            embed: discord.Embed = fail_embed("User is not muted. ")
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        await user.remove_roles(role)
        
        embed: discord.Embed = success_embed(
            f"**{user.mention}** unmuted."
        )
        await inter.response.send_message(embed=embed)

    
#--------------------------------------------------------------------------------------------------------------------------
    # @someone

    @app_commands.command(
        name="someone",
        description="Mentions a random user.",
    )
    @app_commands.default_permissions(mention_everyone=True)
    async def someone(self, inter: discord.Interaction) -> None: 
        """ Ping a random user """

        # getting a list that contains all non-bot members
        members: list = []
        for m in inter.guild.members:
            if not m.bot:
                members.append(m)
        
        # sending a random one from that list
        rnd: int = randint(0, len(members) - 1)
        await inter.delete_original_response()
        await inter.channel.send(members[rnd].mention)


#--------------------------------------------------------------------------------------------------------------------------
    # sudo command
    
    @app_commands.command(
        name="sudo",
        description="Sends a message as the bot.",
    )
    @app_commands.default_permissions(mention_everyone=True)
    async def sudo(self, inter: discord.Interaction, message: str) -> None:
        """ Send a message as the bot """
        
        await inter.channel.send(message)
        await inter.response.send_message("Done.")
        await inter.delete_original_response()
    

#--------------------------------------------------------------------------------------------------------------------------
    # kick commands

    @app_commands.command(
        name="kick",
        description="Kicks a user.",
    )
    @app_commands.default_permissions(kick_members=True)
    async def kick(
            self, inter: discord.Interaction,
            user: discord.Member, reason: Optional[str] = None) -> None:
        """ Kick a user """
        
        # cannot kick me
        if user.id == users["porl"]:
            await inter.response.send_message(
                embed=fail_embed("**L**")
            )
            return
        
        # kick the user
        await user.kick(reason=str(reason))
        
        embed: discord.Embed = success_embed(
            f"**{user.mention}** has been kicked for {reason}."
        )
        embed.set_footer(text=f"Kicked by {inter.user.name}")
        await inter.response.send_message(embed=embed)



#--------------------------------------------------------------------------------------------------------------------------
    # ban command:

    @app_commands.command(
        name="ban",
        description="Bans a user.",
    )
    @app_commands.default_permissions(ban_members=True)
    async def ban(
            self, inter: discord.Interaction,
            user: discord.Member, reason: Optional[str] = None) -> None:
        """ Bans a user """

        # if trying to ban me
        if user.id == users["porl"]:
            await inter.response.send_message(
                embed=fail_embed("**L**")
            )
            return

        # ban the user
        await user.ban(reason=str(reason), delete_message_days=0)
        
        # send them a silly message
        try:
            await user.send(
                f"You've been banned from {inter.guild.name}\nLLLLLLLLL"
            )
        except (discord.app_commands.errors.CommandInvokeError, discord.errors.HTTPException) as e:
            print("Unable to message user (blocked or bot account)")
        
        
        embed: discord.Embed = success_embed(
            f"**{user.mention}** has been banned for {reason}."
        )
        embed.set_footer(text=f"Banned by {inter.user.name}")
        await inter.response.send_message(embed=embed)
    

#--------------------------------------------------------------------------------------------------------------------------
    # purge

    @app_commands.command(
        name="purge",
        description="Purges an amount of messages.",
    )
    @app_commands.default_permissions(manage_messages=True)
    async def purge(self, inter: discord.Interaction, limit: int) -> None:
        """ Deletes an amount of messages """
        
        if limit > 50:
            embed: discord.Embed = fail_embed("Too many messages")
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        await inter.channel.purge(limit=(limit+1))
        
        embed: discord.Embed = success_embed(f"**{limit}** messages cleared.")
        embed.set_footer(text=f"Purged by {inter.user.name}")
        await inter.channel.send(embed=embed)
        

#--------------------------------------------------------------------------------------------------------------------------
    #nick command
    
    @app_commands.command(
        name="nick",
        description="Changes the nick of a user.",
    )
    @app_commands.default_permissions(manage_nicknames=True)
    async def nick(
            self, inter: discord.Interaction,
            user: discord.Member, nick: str) -> None:
        """ Nick a user """

        new_user = await user.edit(nick=nick)
        
        embed: discord.Embed = success_embed(
            f"Nickname changed to **{nick}**."
        )
        embed.set_footer(text=f"Nicked by {inter.user.name}")
        await inter.response.send_message(embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    #warn command

    @app_commands.command(
        name="warn",
        description="Warns a user.",
    )
    async def warn(
            self, inter: discord.Interaction,
            user: discord.Member, reason: str) -> None:
        """ Warns a user """
        await inter.response.send_message(".....")
        
        # cannot warn without the mod role
        mod_role: discord.Role = get(inter.guild.roles, id=roles["mod"])
        if mod_role not in inter.user.roles:
            embed: discord.Embed = fail_embed("Invalid permissions")
            await inter.response.send_message(embed=embed, ephemeral=True)
            return
        
        # cannot warn yourself or a bot
        if user == inter.user or user.bot:
            embed: discord.Embed = fail_embed("Invalid user")
            await inter.response.send_message(embed=embed, ephemeral=True)
            return 
        
        embed: discord.Embed = success_embed(
            f"{user.mention} has been warned for '{reason}'"
        )
        embed.set_footer(text=f"Warned by {inter.user.display_name}")
        await inter.edit_original_response(content=None, embed=embed)


#--------------------------------------------------------------------------------------------------------------------------
    # lockdown 
    
    @app_commands.command(
        name="lockdown",
        description="Locks down a channel",
    )
    @app_commands.default_permissions(manage_channels=True)
    async def lock(self, inter: discord.Interaction) -> None:
        """ Locks a channel down """
        
        # locks the channel
        await inter.channel.set_permissions(
            inter.guild.default_role, 
            send_messages=False,
            add_reactions=False,
        )
        
        embed: discord.Embed = success_embed(
            f"<#{inter.channel.id}> has been locked."
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
        """ Unlocks a channel """
        
        # unlocks a channel
        await inter.channel.set_permissions(
            inter.guild.default_role, 
            send_messages=True,
            add_reactions=True,
        )
        
        embed: discord.Embed = success_embed(
            f"<#{inter.channel.id}> has been unlocked."
        )
        embed.set_footer(text=f"Unlocked by {inter.user.name}")
        await inter.response.send_message(embed=embed)
        

#--------------------------------------------------------------------------------------------------------------------------

  
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Moderator(bot))
