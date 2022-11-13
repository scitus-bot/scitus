"""
Die
Respawn
"""

import discord
from discord.ext import commands
from discord.utils import get
from discord import app_commands
from random import randint
from pasta import ListsPas, RoleIDs, UserIDs
import subprocess 
import sys



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
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def is_porl() -> None:
        def predicate(interaction: discord.Interaction) -> bool:
            return interaction.user.id == UserIDs.porlUserID or interaction.user.id == UserIDs.ninAltUserID
        return app_commands.check(predicate)

#--------------------------------------------------------------------------------------------------------------------------
    #respawn command (when i inevitably lose all my roles)

    @app_commands.command(
        name="respawn",
        description="Gives me roles (testing).",
    )
    @is_porl()
    async def respawn(self, inter: discord.Interaction) -> None:

        roleIds = [
            RoleIDs.adminRoleID,
            RoleIDs.modRoleID, 
            RoleIDs.porlRoleID,
            ] 

        for roleId in roleIds:
            await inter.user.add_roles(get(inter.guild.roles, id=roleId))

        await inter.response.send_message("https://cdn.discordapp.com/attachments/709182248741503093/856158394292895754/swag.gif")


#--------------------------------------------------------------------------------------------------------------------------
    #removes my roles
    #for testing purposes

    @app_commands.command(
        name="die",
        description="Removes my roles (testing).",
    )
    @is_porl()
    async def die(self, inter: discord.Interaction) -> None:

        roleIds = [
            RoleIDs.adminRoleID, 
            RoleIDs.modRoleID, 
            RoleIDs.porlRoleID, 
            RoleIDs.mutedRoleID,
            ] 

        for roleId in roleIds:
            await inter.user.remove_roles(get(inter.guild.roles, id=roleId))

        await inter.response.send_message("https://cdn.discordapp.com/emojis/814109742607630397.gif?v=1")


#--------------------------------------------------------------------------------------------------------------------------
# update command # real
    
    # @commands.command(
    #     help="Updates the bot",
    # )
    # @commands.cooldown(1, 20, BucketType.user)
    # async def update(self, ctx):
    #     if ctx.author.id != UserIDs.porlUserID:
    #         return

    #     await ctx.channel.send("Updating the bot...")


    #     try:
    #         subprocess.Popen(["./scitusupdate.sh"]) # runs the script saved on the server
    #         # saves the last commit into a file
    #         with open("last_sha.txt", "w") as op:
    #             repo = git.Repo("~/scitus")
    #             sha = repo.head.object.hexsha[:7]
    #             op.write(str(sha))
    #     except:
    #         await ctx.channel.send(f"Error encountered.")
    #     else:
    #         sys.exit()  # to prevent any possible clashes 

    # @update.error
    # async def update_error(self, ctx, error):
    #     await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------
    # logout command

    @app_commands.command(
        name="logout",
        description="Logs out the bot.",
    )
    @is_porl()
    async def logout(self, inter: discord.Interaction) -> None:
            
        embed: discord.Embed = discord.Embed(
            title="Success", 
            colour=discord.Colour.green(),
            description=f"Logging out the bot.",
        )
        await inter.response.send_message(embed=embed)
        sys.exit()


#--------------------------------------------------------------------------------------------------------------------------
    # version command

    # @commands.command(
    #     help="Returns the last short sha that the bot was updated on."
    # )
    # @commands.cooldown(1, 20, BucketType.user)
    # async def version(self, ctx):
    #     with open("last_sha.txt", "r") as rf:
    #         sha = rf.read()
    #         await ctx.channel.send(f"The last commit that the bot was updated on is: {sha}")


    # @version.error
    # async def version_error(self, ctx, error):
    #     await handleError(ctx, error)


#--------------------------------------------------------------------------------------------------------------------------

# adds the cog to the main.py and allows it to be used
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Porl(bot))