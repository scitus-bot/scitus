import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from random import randint
from pasta import ListsPas
import requests as r
import os
from dotenv import load_dotenv
load_dotenv()

WH_URL = os.environ.get('URL')


#No "has_role"s


"""
editrole
-colour
-name
-delete
applyall
"""
CDOWN = 20 # cooldown time


async def handleError(message, error): # im glad this works
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


#--------------------------------------------------------------------------------------------------------------------------
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.group(
        help="Edits a role", 
        )
    
    async def editrole(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send("Command can't be used without subcommand.")


#--------------------------------------------------------------------------------------------------------------------------
    #colour
    
    @editrole.command(
        help="Changes the colour of a role.",
        brief="Changes the colour of a role.",
        )
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, CDOWN, BucketType.user)
    async def colour(self, ctx, role: discord.Role, colour):
        colour = int(colour, base=16)
        colour = discord.Colour(colour)
        await role.edit(colour=colour)
        await ctx.channel.send(f"Role colour changed to {str(colour)}")


    @colour.error
    async def colour_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    #name
    
    @editrole.command(
        help="Changes the name of a role.",
        brief="Changes the name of a role.",
        )
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, CDOWN, BucketType.user)
    async def name(self, ctx, role: discord.Role, *name):
        actualName = list(name)
        realActualName = " ".join(actualName)
        await role.edit(name=str(realActualName))
        await ctx.channel.send(f"Role name changed to {realActualName}")


    @name.error
    async def name_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    # delete role
    
    @editrole.command(
        help = "Deletes a role >:)",
        )
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, CDOWN, BucketType.user)
    async def delete(self, ctx, role: discord.Role):
        roleName = role.name()
        await role.delete()
        await ctx.channel.send(f"@{roleName} has been deleted.")


    @delete.error
    async def delete_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
  # applyall

    @commands.command(
        help="Gives everyone in the server a role",
        )
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, CDOWN, BucketType.user)
    async def giveall(self, ctx, role: discord.Role):
        
        # giving all non-bot users a role
        for member in ctx.guild.members:
            if not member.bot:
                await member.add_roles(role)
            else:
                print(f"{member.name} is a bot")
        ctx.channel.send("Succesfully gave everyone the role.")


    @giveall.error
    async def giveall_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    # removeall

    @commands.command(
        help="Removes a role from everyone",
        )
    @commands.has_permissions(manage_roles=True)
    @commands.cooldown(1, CDOWN, BucketType.user)
    async def removeall(self, ctx, role: discord.Role):
        
        # removing a role from all non-bot users
        for member in ctx.guild.members:
            if not member.bot:
                await member.remove_roles(role)
            else:
                print(f"{member.name} is a bot")
        
        ctx.channel.send("Succesfully removed the role from everyone.")


    @removeall.error
    async def removeall_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    # send as webhook

    @commands.command(
        help="Sends a message as a webhook",
        )
    @commands.has_permissions(
        manage_messages=True,
        manage_webhooks=True,
        )
    @commands.cooldown(1, CDOWN, BucketType.user)
    async def sudow(self, ctx): # will add username/pfp support later on 
        """ Sends a message as a webhook. """
        print(ctx.author.name)

        # takes the whole message as a list, removes the ",sudow" part and then
        # the bot sends that
        msg = ctx.message.content
        messageArray = msg.split()
        del messageArray[0]
        message = " ".join(messageArray)
        
        message = "** **" if message == "" else message
        
        data = {
            "content": message,         
        }
        
        await ctx.message.delete()
        r.post(WH_URL, json=data)
        
        
    @sudow.error
    async def sudow_error(self, ctx, error):
        await handleError(ctx, error)

#--------------------------------------------------------------------------------------------------------------------------

#necessities

def setup(bot):
  bot.add_cog(Admin(bot))