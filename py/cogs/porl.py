#importing stuff
import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import cooldown, BucketType
import random
from pasta import *

"""
Die
Respawn
"""


class Porl(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


async def handleError(error, ctx):
  if isinstance(error, commands.CommandOnCooldown):
    msg = 'This command is on cooldown, please try again in {:.2f}s'.format(error.retry_after)
    await ctx.channel.send(msg)
  else:
    raise error


#--------------------------------------------------------------------------------------------------------------------------
#respawn command (when i inevitably lose all my roles)

  @commands.command(
    help="Adds the admin/mod/personal role back to me if it ever gets removed.",
    brief="Gives roles back to Porl.",
    case_insensitive = True
  )
  @commands.cooldown(1, 60, commands.BucketType.guild)
  async def respawn(self, ctx):
    #try:
      if ctx.author.id != userIDS.porlUserID:
        await ctx.channel.send("You are not the chosen one")
        return

      roleIds = [roleIDS.adminRoleID,
                roleIDS.modRoleID, 
                roleIDS.porlRoleID] 

      for roleId in roleIds:
        await ctx.author.add_roles(get(ctx.author.guild.roles, id=roleId))

      await ctx.channel.send("https://cdn.discordapp.com/attachments/709182248741503093/856158394292895754/swag.gif")

  @respawn.error
  async def respawn_error(self, ctx, error):
    await handleError(error, ctx)
    #except CommandOnCooldown(bucket, retry_after):
    #  await ctx.channel.send("bro calm down")

#end of command



#--------------------------------------------------------------------------------------------------------------------------
#removes my roles
#for testing purposes

  @commands.command(
    help="Removes admin/mod/personal role. Used for testing.",
    brief="Removes roles, used for testing.",
    case_insensitive = True
  )
  @commands.cooldown(1, 60, commands.BucketType.guild)
  async def die(self, ctx):
    #try:
      if ctx.author.id != userIDS.porlUserID:
        await ctx.channel.send("You are not the chosen one")
        return

      roleIds = [roleIDS.adminRoleID, 
                roleIDS.modRoleID, 
                roleIDS.porlRoleID, 
                roleIDS.mutedRoleID] 

      for roleId in roleIds:
        await ctx.author.remove_roles(get(ctx.author.guild.roles, id=roleId))

      await ctx.channel.send("https://cdn.discordapp.com/emojis/814109742607630397.gif?v=1")

  @die.error
  async def die_error(self, ctx, error):
    await handleError(error, ctx)


#end of command
#--------------------------------------------------------------------------------------------------------------------------



#necesseties
def setup(bot):
  bot.add_cog(Porl(bot))