#importing
import discord
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from random import randint
import pasta



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
async def handleError(error, ctx): 
    # idk if doing this asynchronously will make any errors or not but im willing to find out
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again in {:.2f}s'.format(error.retry_after)
        await ctx.channel.send(msg)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")
    elif isinstance(error, commands.MissingRole):
        await ctx.channel.send("You cant do that!")
    elif isinstance(error, commands.MissingRequiredArgument):
        rnd = randint(0, len(pasta.listsPas.helpPastas) - 1)
        await ctx.channel.send(pasta.listsPas.helpPastas[rnd])
    else:
        raise error



#--------------------------------------------------------------------------------------------------------------------------
class Moderator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


#--------------------------------------------------------------------------------------------------------------------------
    #mute command
    
    @commands.command(
        help="Adds the Muted role to a target",
        brief="Mute command",
        case_insensitive = True,
        aliases=["mute"],
        )
    @commands.has_role(pasta.roleIDS.modRoleID) #mod role
    @commands.cooldown(1, 3, commands.BucketType.guild)
    async def eject(self, ctx, member : discord.Member): #arguments in the command

        if ctx.author == member: #prevent users from muting themselves
            await ctx.channel.send("You are not the imposter.")
        else:
            role = get(ctx.author.guild.roles, id=pasta.roleIDS.mutedRoleID) #getting the role (doesnt work)
            #wouldnt it be so fucking funny if this worked
            if role in member.roles:
                await ctx.channel.send("This person is already ejected.")
            else:
                await member.add_roles(role) #meant to add the role to the meember
                await ctx.channel.send(f"{member} was the imposter.")


    @eject.error
    async def eject_error(self, ctx, error):
        await handleError(error, ctx)


#--------------------------------------------------------------------------------------------------------------------------
    #unmute command
    
    @commands.command(
        help="Removes the Muted role.",
        brief="Unmute command",
        case_insensitive = True,
        )
    @commands.has_role(pasta.roleIDS.modRoleID) #mod role
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def unmute(self, ctx, member : discord.Member): #ctx is just a variable
        if ctx.author == member: #prevent users from unmuting themselves
            await ctx.channel.send("You cannot unmute yourself.")
        else:
            muted = get(ctx.author.guild.roles, id=pasta.roleIDS.mutedRoleID) #removes mute role
            #print(muted)

            if muted in member.roles:
                await member.remove_roles(muted)
                await ctx.channel.send(f"{member} you have been freed.")

            else:
                await ctx.channel.send("This user is not muted.")

    
    @unmute.error
    async def unmute_error(self, ctx, error):
        await handleError(error, ctx)


#--------------------------------------------------------------------------------------------------------------------------
    #@someone

    @commands.command(
        pass_content=True,
        help="Mentions a random user from the server.",
        brief="Mentions a random user.",
        case_insensitive = True
        )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def someone(self, ctx): #fucking CJ and his spaces for indentation
        #have to rewrite this shit bc of the "inconsistent" indents
        #getting a list of all member IDs
        members = []
        async for member in ctx.guild.fetch_members(limit=None): 
            if not member.bot:  
                members.append(member)


        rnd = randint(0, len(members) - 1)
        await ctx.message.delete()
        await ctx.channel.send(members[rnd].mention)
        # before i edited there were other things down here, but i dont remember what they were/were used for
        # it was to delete the message lol


    @someone.error 
    async def someone_error(self, ctx, error):
        await handleError(error, ctx)


#--------------------------------------------------------------------------------------------------------------------------
    #sudo command
    
    @commands.command(
        help="Sends a message, as the bot. Deletes the original message.",
        brief="Output text as the bot.",
        case_insensitive = True,
        )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_role(pasta.roleIDS.modRoleID) #mod command
    async def sudo(self, ctx):
        msg = ctx.message.content
        print(ctx.author.name)
        messageArray = msg.split()
        del messageArray[0]
        message = " ".join(messageArray)
        await ctx.channel.send(message) #oh yeah lmao ##goddamn
        await ctx.message.delete()
    

    @sudo.error
    async def sudo_error(self, ctx, error):
        await handleError(error, ctx)


#--------------------------------------------------------------------------------------------------------------------------
    #kick commands

    @commands.command(
        help="Kicks a user, innapropriate usage of this command will get you punished uwu",
        brief="Kicks a user.",
        case_insensitive = True,
        )
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def kick(self, ctx, user : discord.Member, *, reason=None):
        await user.kick(reason=str(reason))

        await ctx.channel.send(f"{user.mention} has been kindly removed by {ctx.message.author.mention} <:wholesome:806907457342930975> \n Reason: " + str(reason))
        await ctx.message.delete()


    @kick.error
    async def kick_error(self, ctx, error):
        await handleError(error, ctx)


#--------------------------------------------------------------------------------------------------------------------------
    #ban command:

    @commands.command(
        help="Bans a user uwu",
        brief="Bans a user.",
        case_insensitive = True
        )
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def ban(self, ctx, user : discord.Member, *, reason=None):
        await user.ban(reason=str(reason), delete_message_days=0)
        await user.send("You've been banned from Monkeys and Dragons\nLLLLLLLLL")
        await ctx.channel.send(f"{user.mention} has left. {ctx.message.author.mention} <:peepoSad:809355473831854132> \n Reason: {str(reason)}")
        await ctx.message.delete()


    @ban.error
    async def ban_error(self, ctx, error):
        await handleError(error, ctx)
    

#--------------------------------------------------------------------------------------------------------------------------
    #purge

    @commands.command(
        pass_context=True,
        help="Purges a given amount of messages.",
        brief="Purges messages.",
        )
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def purge(self, ctx, limit: int):
        if limit > 30:
            await ctx.channel.send("Purge less messages dipshit")
            return
        limit = limit + 1
        await ctx.channel.purge(limit=limit)
        await ctx.send(str(limit - 1) + ' messages cleared by {}'.format(ctx.author.mention))


    @purge.error
    async def clear_error(self, ctx, error):
        await handleError(error, ctx)
      
      
#--------------------------------------------------------------------------------------------------------------------------
    #nick command
    
    @commands.command(
        pass_context=True, 
        help="Changes the nickname of a user.",
        )
    @commands.has_permissions(manage_nicknames=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nick(self, ctx, user : discord.Member, *nickname):
        if user.id == pasta.userIDS.porlUserID: # so i cant be nick changed (minor trolling)
            await ctx.channel.send("fuck off")
            return

        listNick = list(nickname)
        realNick = " ".join(listNick)
        await user.edit(nick=realNick)
        await ctx.channel.send("Nickname changed.")


    @nick.error
    async def nick_error(self, ctx, error):
        await handleError(error, ctx)


#--------------------------------------------------------------------------------------------------------------------------
    #warn command

    @commands.command(
        pass_context=True,
        help="Warns a user.",
        )
    @commands.has_role(pasta.roleIDS.modRoleID) #mod
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def warn(self, ctx, user : discord.Member):
        if ctx.author.id == user.id:
            await ctx.channel.send("You can't warn yourself dipshit")
        else:
            await ctx.channel.send(f"{user.mention} has been warned.")


    @warn.error
    async def warn_error(self, ctx, error):
        await handleError(error, ctx)


#--------------------------------------------------------------------------------------------------------------------------
    # lockdown 
    
    @commands.command(
        pass_context=True,
        case_insensitive=True,
        help="Locks down a channel.",
        )
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(
            ctx.guild.default_role, 
            send_messages=False,
            add_reactions=False,
            )
        await ctx.channel.send("Channel locked 👍")


    @lock.error
    async def lock_error(self, ctx, error):
        await handleError(error, ctx)
        
        
#--------------------------------------------------------------------------------------------------------------------------
    # unlockdown
    
    @commands.command(
        pass_context=True,
        case_insensitive=True,
        help="Unlocks a channel",
        )
    @commands.has_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(
            ctx.guild.default_role, 
            send_messages=True,
            add_reactions=True,
            )
        await ctx.channel.send("Channel unlocked 👍")
        

    @unlock.error
    async def unlock_error(self, ctx, error):
        await handleError(error, ctx)
        
        
#--------------------------------------------------------------------------------------------------------------------------


  
# this bit is just necessary i should probably look into why
def setup(bot):
    bot.add_cog(Moderator(bot))