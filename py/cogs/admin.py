import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import cooldown, BucketType
import random
import pasta


#holy shit this could be a massive mistake
#No "has_role"s

# setnick command isnt needed bc you can just pass the bot through the nick command

"""
editrole
-colour
-name
-delete
applyall
"""
cdown = 20 # cooldown time


# there fucking has to be a better way to do this


async def handleError(error, message): # im glad this works
  if isinstance(error, commands.CommandOnCooldown):
    msg = 'This command is on cooldown, please try again in {:.2f}s'.format(error.retry_after)
    await message.channel.send(msg)
  elif isinstance(error, commands.MissingPermissions):
      await message.send("You cant do that!")
  elif isinstance(error, commands.MissingRequiredArgument):
    await message.channel.send(pasta.listsPas.helpPastas[random.randrange(0, len(pasta.listsPas.helpPastas) - 1)])
    raise error
  else:
    raise error


#--------------------------------------------------------------------------------------------------------------------------
class Admin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None


  @commands.group(
    help="Edits a role" 
  )
  async def editrole(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.channel.send("Command can't be used without subcommand.")

#--------------------------------------------------------------------------------------------------------------------------
  #colour
  @editrole.command(
    help="Changes the colour of a role.",
    brief="Changes the colour of a role.",
    case_insensitive = True
  )
  @commands.has_permissions(manage_roles=True)
  @commands.cooldown(1, cdown, commands.BucketType.user)
  async def colour(self, ctx, role : discord.Role, colour):
    colour = int(colour, base=16)
    colour = discord.Colour(colour)
    await role.edit(colour=colour)
    await ctx.channel.send(f"Role colour changed to {str(colour)}")


  @colour.error
  async def colour_error(self, ctx, error):
    await handleError(error, ctx)


#--------------------------------------------------------------------------------------------------------------------------
  #name
  @editrole.command(
    help="Changes the name of a role.",
    brief="Changes the name of a role.",
    case_insensitive = True
  )
  @commands.has_permissions(manage_roles=True)
  @commands.cooldown(1, cdown, commands.BucketType.user)
  async def name(self, ctx, role : discord.Role, *name):
    actualName = list(name)
    realActualName = " ".join(actualName)
    await role.edit(name=str(realActualName))
    await ctx.channel.send(f"Role name changed to {realActualName}")

  @name.error
  async def name_error(self, ctx, error):
    await handleError(error, ctx)

#--------------------------------------------------------------------------------------------------------------------------

  @editrole.command(
    help = "Deletes a role >:)",
    case_insensitive = True 
  )
  @commands.has_guild_permissions(manage_roles=True)
  @commands.cooldown(1, cdown, commands.BucketType.user)
  async def delete(self, ctx, role : discord.Role):
    roleName = role.name()
    await role.delete()
    await ctx.channel.send(f"@{roleName} has been deleted.")

  @delete.error
  async def delete_error(self, ctx, error):
    await handleError(error, ctx)

#--------------------------------------------------------------------------------------------------------------------------

  """ 
  @commands.command(
    help="Hopefully an eval command",
    case_insenstive=True
  )
  @commands.has_role(pasta.roleIDS.adminRoleID)
  @commands.cooldown(1, cdown, commands.BucketType.user)
  async def eval(ctx, k*, command):
    rt = spidermonkey.Runtime()
    cx = rt.new_context()
    result = cx.eval_script(command)
    return await result
   """
#--------------------------------------------------------------------------------------------------------------------------
  # applyall command

  @commands.command(
    help="Gives everyone in the server a role",
    case_insensitive=True
  )
  @commands.has_permissions(manage_roles=True)
  @commands.cooldown(1, cdown, commands.BucketType.user)
  async def giveall(self, ctx, role : discord.Role):
    members =[]
    async for member in ctx.guild.fetch_members(limit=None):
      if not member.bot:
        await member.add_roles(role)
      else:
        print(f"{member.name} is a bot")





#--------------------------------------------------------------------------------------------------------------------------

#necessities
def setup(bot):
  bot.add_cog(Admin(bot))