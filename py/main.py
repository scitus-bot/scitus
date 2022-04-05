#summoning modules and shit
import os
import discord
from discord.ext import commands
from discord.utils import get
from keep_alive import keep_alive
import pasta

#print(datetime.today().weekday())
#monday = 0, sunday = 6

#holy shit so many fucking libraries

#this was a test, this works
#"copypastas" is a class from the file pasta.py
#print(copypastas.vaporeonPas)


# annoying as fuck thing ratelimiting my code
# i think its the autofilter but im not sure


#--------------------------------------------------------------------------------------------------------------------------
#weird stuff i dont get
my_secret = os.environ['TOKEN']
#token is unique, cant give that to you

#weird stuff
prefix = pasta.prefixPasta #change prefix in pasta.py
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(intents=intents, command_prefix=prefix, case_insensitive=True,)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your mum"))
#--------------------------------------------------------------------------------------------------------------------------
#no clue what im doing, but its something to do with cogs

initial_extensions = ["cogs.everyone", #everyone commands
                      "cogs.mod",      #mod commands
                      "cogs.porl",      #porl commands
                      "cogs.admin",  #admin commands
                      "cogs.hive"]     #hive commands

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


#--------------------------------------------------------------------------------------------------------------------------
#on_message thing

@bot.event
async def on_message(msg):
  msgContent = msg.content
  
  """ 
  if msg.author.id == 251066113679425537:
    await msg.delete()
    ninsang = bot.get_user(251066113679425537)
    await ninsang.send("L")
  """
  
  
  #if i get pinged, it will tell them to shut up # (removed)
  mentioned = msg.mentions
  for user in mentioned:
    if msg.author.bot: # bot
      return
    
    elif user.id == 848209731474817094: #bot
      porl = bot.get_user(409821972026097667)
      await porl.send(f"{msgContent} - sent by - {msg.author.mention}")

  # next # uncommented this line of code

#--------------------------------------------------------------------------------------------------------------------------

  #AUTOREPLY (copypastas)
  #finding how to do case insensitive things 
  if msg.author.bot:
     return
  else:
    if "vaporeon" in msg.content.lower(): #Green squigglies show up but you can ignore them.
      await msg.channel.send(pasta.copypastas.vaporeonPas, delete_after=20.0)

    if "gaming laptop" in msg.content.lower():
      await msg.channel.send(pasta.copypastas.laptopPas, delete_after=20.0)

    if "meow" in msg.content.lower():
      await msg.channel.send(pasta.copypastas.meowPas, delete_after=20.0)

    if "downvote" in msg.content.lower():
      await msg.channel.send(pasta.copypastas.downfaqPas, delete_after=20.0)

    if "dog" in msg.content.lower() and "doggo" not in msg.content.lower():
        await msg.channel.send(pasta.copypastas.doggoPas, delete_after=20.0)

#--------------------------------------------------------------------------------------------------------------------------
    #autofilter:
    for word in pasta.listsPas.autoMutePas:
      if word in msgContent:
        await msg.delete()
        await msg.channel.send(f"{msg.author.mention} you can't send that!")

  await bot.process_commands(msg)

#--------------------------------------------------------------------------------------------------------------------------
## wow nice
#necessities

keep_alive()
bot.run(my_secret)