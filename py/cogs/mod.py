import discord
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import BucketType
from random import randint
from pasta import ListsPas, RoleIDs, UserIDs

"""
List of commands:
  -Silence
  -Free
  -Sudo
  -Someone 
  -purge
  -nick
"""


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
    def __init__(self, bot):
        self.bot = bot


#--------------------------------------------------------------------------------------------------------------------------
    #mute command
    
    @commands.command(
        help="Adds the Muted role to a target",
        brief="Mute command",
        aliases=["mute"],
        )
    @commands.has_role(RoleIDs.modRoleID)   #mod role
    @commands.cooldown(1, 3, BucketType.guild)
    async def eject(self, ctx, member: discord.Member):
        """ Mutes a member if they've been naughty. """
        if ctx.author == member:            # prevent self-muting
            await ctx.channel.send("You are not the imposter.")
            return

        
        role = get(ctx.guild.roles, id=RoleIDs.mutedRoleID)
        if role in member.roles:
            await ctx.channel.send("This person is already ejected.")
        else:
            await member.add_roles(role)
            await ctx.channel.send(f"{member} was the imposter.")


    @eject.error
    async def eject_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    # unmute command
    
    @commands.command(
        help="Removes the Muted role.",
        brief="Unmute command",
        )
    @commands.has_role(RoleIDs.modRoleID)   # mod role
    @commands.cooldown(1, 10, BucketType.guild)
    async def unmute(self, ctx, member : discord.Member):
        """ Unmutes a member if they're muted. """
        if ctx.author == member:        # prevent self-unmuting
            await ctx.channel.send("You cannot unmute yourself.")
            return
        

        role = get(ctx.guild.roles, id=RoleIDs.mutedRoleID)     # the muted role
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.channel.send(f"{member} you have been freed.")
        else:
            await ctx.channel.send("This user is not muted.")

    
    @unmute.error
    async def unmute_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    #@someone

    @commands.command(
        help="Mentions a random user from the server.",
        brief="Mentions a random user.",
        )
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def someone(self, ctx): 
        """ Pings a random member in the current server """

        # getting a list that contains all non-bot members
        members = []
        for m in ctx.guild.members:
            if not m.bot:
                members.append(m)
        

        rnd = randint(0, len(members) - 1)
        await ctx.message.delete()
        await ctx.channel.send(members[rnd].mention)


    @someone.error 
    async def someone_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    #sudo command
    
    @commands.command(
        help="Sends a message, as the bot. Deletes the original message.",
        brief="Output text as the bot.",
        )
    @commands.has_role(RoleIDs.modRoleID) 
    @commands.cooldown(1, 3, BucketType.user)
    async def sudo(self, ctx):
        """ Sends a message as the bot. """
        print(ctx.author.name)

        # takes the whole message as a list, removes the ",sudo" part and then
        # the bot sends that
        msg = ctx.message.content
        messageArray = msg.split()
        del messageArray[0]
        message = " ".join(messageArray)
        
        if message == "":
            await ctx.channel.send("** **")
        else:
            await ctx.channel.send(message) 
            
        await ctx.message.delete()
    

    @sudo.error
    async def sudo_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    #kick commands

    @commands.command(
        help="Kicks a user, innapropriate usage of this command will get you punished uwu",
        brief="Kicks a user.",
        )
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 20, BucketType.user)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        """ Kicks a user. """
        await user.kick(reason=str(reason))

        await ctx.channel.send(f"{user.mention} has been kindly removed by {ctx.author.mention} <:wholesome:806907457342930975> \n Reason: {str(reason)}")
        await ctx.message.delete()


    @kick.error
    async def kick_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    #ban command:

    @commands.command(
        help="Bans a user uwu",
        brief="Bans a user.",
        )
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 20, BucketType.user)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        """ Bans a member. """
        await user.ban(reason=str(reason), delete_message_days=0)
        await user.send(f"You've been banned from {ctx.guild.name}\nLLLLLLLLL")
        await ctx.channel.send(f"{user.mention} has left. {ctx.author.mention} <:peepoSad:809355473831854132> \n Reason: {str(reason)}")
        await ctx.message.delete()


    @ban.error
    async def ban_error(self, ctx, error):
        await handleError(ctx, error)
    

#--------------------------------------------------------------------------------------------------------------------------
    #purge

    @commands.command(
        help="Purges a given amount of messages.",
        brief="Purges messages.",
        )
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def purge(self, ctx, limit: int):
        """ Purges a certain amount of messages """
        if limit > 30:
            await ctx.channel.send("Purge less messages dipshit")
            return

        await ctx.channel.purge(limit=(limit+1))
        await ctx.channel.send(f"{limit} messages cleared by {ctx.author.mention}")
        

    @purge.error
    async def clear_error(self, ctx, error):
        await handleError(ctx, error)
      
      
#--------------------------------------------------------------------------------------------------------------------------
    #nick command
    
    @commands.command(
        help="Changes the nickname of a user.",
        )
    @commands.has_permissions(manage_nicknames=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def nick(self, ctx, user: discord.Member, *nickname):
        """ Changes the nickname of a user. """
        if user.id == UserIDs.porlUserID: # so i cant be nick changed (minor trolling)
            await ctx.channel.send("fuck off")
            return

        listNick = list(nickname)
        realNick = " ".join(listNick)
        await user.edit(nick=realNick)
        await ctx.channel.send("Nickname changed.")


    @nick.error
    async def nick_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    #warn command

    @commands.command(
        help="Warns a user.",
        )
    @commands.has_role(RoleIDs.modRoleID) 
    @commands.cooldown(1, 5, BucketType.user)
    async def warn(self, ctx, user: discord.Member):
        """ Warns a user, in reality does nothing. """
        if ctx.author.id == user.id:
            await ctx.channel.send("You can't warn yourself dipshit")
            return 
        
        await ctx.channel.send(f"{user.mention} has been warned.")


    @warn.error
    async def warn_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    # lockdown 
    
    @commands.command(
        help="Locks down a channel.",
        )
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def lock(self, ctx):
        """ Locks the channel that the command was used in so only mods can send messages """
        await ctx.channel.set_permissions(
            ctx.guild.default_role, 
            send_messages=False,
            add_reactions=False,
            )
        await ctx.channel.send("Channel locked 👍")


    @lock.error
    async def lock_error(self, ctx, error):
        await handleError(ctx, error)
        
        
#--------------------------------------------------------------------------------------------------------------------------
    # unlockdown
    
    @commands.command(
        help="Unlocks a channel",
        )
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def unlock(self, ctx):
        """ Unlocks the channel that this was sent in. """
        await ctx.channel.set_permissions(
            ctx.guild.default_role, 
            send_messages=True,
            add_reactions=True,
            )
        await ctx.channel.send("Channel unlocked 👍")
        

    @unlock.error
    async def unlock_error(self, ctx, error):
        await handleError(ctx, error)
        
        
#--------------------------------------------------------------------------------------------------------------------------


  
# this bit is just necessary i should probably look into why
def setup(bot):
    bot.add_cog(Moderator(bot))