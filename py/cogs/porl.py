import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import BucketType
from random import randint
from pasta import ListsPas, RoleIDs, UserIDs
import subprocess 
import sys
import git

"""
Die
Respawn
"""




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

class Porl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#--------------------------------------------------------------------------------------------------------------------------
    #respawn command (when i inevitably lose all my roles)

    @commands.command(
        help="Adds the admin/mod/personal role back to me if it ever gets removed.",
        brief="Gives roles back to Porl.",
        )
    @commands.cooldown(1, 60, BucketType.user)
    async def respawn(self, ctx):
        if ctx.author.id == 545959964921823247:
            await ctx.channel.send("Stop using this command!!")

        if ctx.author.id != UserIDs.porlUserID and ctx.author.id != UserIDs.ninAltUserID:
            await ctx.channel.send("You are not the chosen one")
            return

        roleIds = [
            RoleIDs.adminRoleID,
            RoleIDs.modRoleID, 
            RoleIDs.porlRoleID,
            ] 

        for roleId in roleIds:
            await ctx.author.add_roles(get(ctx.author.guild.roles, id=roleId))

        await ctx.channel.send("https://cdn.discordapp.com/attachments/709182248741503093/856158394292895754/swag.gif")


    @respawn.error
    async def respawn_error(self, ctx, error):
        await handleError(ctx, error)
        

#--------------------------------------------------------------------------------------------------------------------------
    #removes my roles
    #for testing purposes

    @commands.command(
        help="Removes admin/mod/personal role. Used for testing.",
        brief="Removes roles, used for testing.",
        )
    @commands.cooldown(1, 60, BucketType.user)
    async def die(self, ctx):
        #try:
        if ctx.author.id != UserIDs.porlUserID and ctx.author.id != UserIDs.ninAltUserID:
            await ctx.channel.send("You are not the chosen one")
            return

        roleIds = [
            RoleIDs.adminRoleID, 
            RoleIDs.modRoleID, 
            RoleIDs.porlRoleID, 
            RoleIDs.mutedRoleID,
            ] 

        for roleId in roleIds:
            await ctx.author.remove_roles(get(ctx.author.guild.roles, id=roleId))

        await ctx.channel.send("https://cdn.discordapp.com/emojis/814109742607630397.gif?v=1")


    @die.error
    async def die_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
# update command # real
    
    @commands.command(
        help="Updates the bot",
    )
    @commands.cooldown(1, 20, BucketType.user)
    async def update(self, ctx):
        if ctx.author.id != UserIDs.porlUserID:
            return

        await ctx.channel.send("Updating the bot...")


        try:
            with open("last_sha.txt", "w") as op:
                repo = git.Repo("~/scitus")
                sha = repo.head.object.hexsha
                op.write(str(sha))

            subprocess.Popen(["./scitusupdate.sh"]) # runs the script saved on the server
        except:
            await ctx.channel.send(f"Error encountered.")
        else:
            sys.exit()  # to prevent any possible clashes 

    @update.error
    async def update_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    # logout command

    @commands.command(
        help="Logs out the bot",
    )
    async def logout(self, ctx):
        if ctx.author.id != UserIDs.porlUserID:
            await ctx.channel.send("Stop being stupid.")
        await ctx.channel.send("Logging out the bot...")
        sys.exit()


    @logout.error
    async def logout_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    # version command

    @commands.command(
        help="Returns the last short sha that the bot was updated on."
    )
    @commands.cooldown(1, 20, BucketType.user)
    async def version(self, ctx):
        with open("last_sha.txt", "r") as rf:
            sha = rf.read()
            await ctx.channel.send(f"The last commit that the bot was updated on is: {sha}")


    @version.error
    async def version_error(self, ctx, error):
        await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------

# adds the cog to the main.py and allows it to be used
def setup(bot):
    bot.add_cog(Porl(bot))