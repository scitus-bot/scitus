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
remindme
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
  #REMINDME COMMAND
  #pretty sure this code is bad, but it does the job
  #it does not L
  
  #It is in slumber until i can be asked to fix it
  #for now ask people to use an alarm on their phones
  
  #attempting to fix this piece of garbage

	#its been fixed


  
  @commands.command(case_insensitive = True,
  help="Reminds you about a thing after a certain amount of time. \n 5s = 5 seconds, 5m = 5 minutes, 5h = 5 hours, 5d = 5 days.",
  brief="Remind you about something after a certain amount of time.") #aliases are pog
  @commands.cooldown(1, 20, commands.BucketType.user)
  async def remindme(self, ctx, after, *, reminder):

    
    async def wait(amount : str, unit, multiplier : int): # for the reminder command
      amount = int(amount.replace(unit, ""))
      sleep(amount*multiplier)


    await ctx.channel.send(f"OK, {ctx.author.mention} I will remind you about '{reminder}' in {after}")


    if after[-1] == "s":
      await wait(after, "s", 1)
    elif after[-1] == "m":
      await wait(after, "m", 60)
    elif after[-1] == "h":
      await wait(after, "h", 3600)
    elif after[-1] == "d":
      await wait(after, "d",86400)


    await ctx.channel.send(f"{ctx.author.mention} --- You are being reminded about '{reminder}'")
      

  @remindme.error
  async def remindme_error(self, ctx, error):
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


  @commands.command(case_insensitive=True)
  @commands.cooldown(1, 20, commands.BucketType.user)
  async def encrypt(self, ctx, code, *mes):
   if len(code) != 4:
    await ctx.channel.send("wrong length bozo")
   else:
    letters = list("QWERTYUIOPASDFGHJKLZXCVBNM")
    mes = " ".join(word for word in mes)
    
    #splitting the code into two different things
    co = int(str(code)[:2])

    de = int(str(code)[2:])

    global newMsg
    newMsg = []

    for i in range(len(mes)):
        global chara
        chara = mes[i].upper()
        if chara not in letters:
          newMsg.append(chara)
          continue 
          #short hand if <3 #CANT USE IT NOOOOO
        #another big if statement woohoo #nvm :trey:
        def newInd(num): #cool function
          newIndex = ord(chara) + num - 64
          while newIndex > 26: newIndex = newIndex - 26
          newMsg.append(chr(newIndex + 64).lower())
    
        newInd(de) if i % 2 == 0 else newInd(co) #short hand if else
    await ctx.message.delete()
    await ctx.channel.send("".join(c for c in newMsg))

  @encrypt.error
  async def encrypt_error(self, ctx, error):
    await handleError(error, ctx)

#necesseties
def setup(bot):
  bot.add_cog(Everyone(bot))