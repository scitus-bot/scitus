import discord
from discord.utils import get
from discord.ext import commands
import asyncio
import random
import pasta
from time import sleep

"""
Ping
Sus  -- Has Cooldown Error
report
"""




# making a function to handle the errors bc i didnt do that before for some reason
async def handleError(error, message): # im glad this works
  if isinstance(error, commands.CommandOnCooldown):
    msg = 'This command is on cooldown, please try again in {:.2f}s'.format(error.retry_after)
    await message.channel.send(msg)

  elif isinstance(error, commands.MissingRequiredArgument):
    await message.channel.send(pasta.listsPas.helpPastas[random.randrange(0, len(pasta.listsPas.helpPastas) - 1)])
    raise error
  
  else:
    raise error



#--------------------------------------------------------------------------------------------------------------------------
class Everyone(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self._last_member = None

  #ping
  @commands.guild_only()
  @commands.command(
    help="Pings the bot to check if its online",
    brief="Responds with 'pong'",
    case_insensitive = True
  )
  @commands.cooldown(1, 5, commands.BucketType.guild)
  async def ping(self, ctx): #here, ping is the command word
    await ctx.channel.send("pong")

  @ping.error
  async def ping_error(self, ctx, error):
    await handleError(error, ctx)
  
  #end of command

#--------------------------------------------------------------------------------------------------------------------------
  #sus
  @commands.command(
    pass_content=True,
    help="ඞ",
    brief="ඞ",
    )
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def sus(self, ctx):
    await ctx.message.delete()
    await ctx.channel.send("ඞ") 
  
  #error thing
  @sus.error
  async def sus_error(self, ctx, error):
    await handleError(error, ctx)

#--------------------------------------------------------------------------------------------------------------------------
  @commands.command(case_insensitive = True,
  help="Use to report people, format like this: Person ID / Reason", brief="Used to report people.")
  @commands.cooldown(1, 20, commands.BucketType.user)
  async def report(self, ctx, userID, *reason):
    reported = userID
    reporter = ctx.author.id
    report = ctx.guild.get_channel(904829118477111366)

    fullReason = ""

    for word in reason:
      fullReason = str(fullReason) + str(word) + " "

    await report.send(f"Reporter: <@!{reporter}> \nReported: {reported} \nReason: {fullReason}")

    await ctx.message.delete()
    await ctx.channel.send("User has been reported!")

  @report.error
  async def report_error(self, ctx, error):
    await handleError(error, ctx)
  
#----------------------------------------------------------------------------------------------------------------

#necesseties
def setup(bot):
  bot.add_cog(Everyone(bot))