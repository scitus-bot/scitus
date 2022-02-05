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


#--------------------------------------------------------------------------------------------------------------------------
#weird stuff i dont get
my_secret = os.environ['TOKEN']
#token is unique, cant give that to you

#weird stuff
prefix = pasta.prefixPasta #change prefix in pasta.py
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(intents=intents, command_prefix=prefix, case_insensitive=True, help_command=False)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

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
async def on_message(message):
  msgContent = message.content
  
  #if i get pinged, it will tell them to shut up
  mentioned = message.mentions
  for user in mentioned:
    if message.author.bot: # bot
      return
    
    elif user.id == 848209731474817094: #bot
      porl = bot.get_user(409821972026097667)
      await porl.send(f"{msgContent} - sent by - {message.author.mention}")

  #next

#--------------------------------------------------------------------------------------------------------------------------

  #AUTOREPLY (copypastas)
  #finding how to do case insensitive things 
  if message.author.bot:
     return
  else:
    if "vaporeon" in message.content.lower(): #Green squigglies show up but you can ignore them.
      await message.channel.send(pasta.copypastas.vaporeonPas, delete_after=20.0)

    if "gaming laptop" in message.content.lower():
      await message.channel.send(pasta.copypastas.laptopPas, delete_after=20.0)

    if "meow" in message.content.lower():
      await message.channel.send(pasta.copypastas.meowPas, delete_after=20.0)

    if "downvote" in message.content.lower():
      await message.channel.send(pasta.copypastas.downfaqPas, delete_after=20.0)

    if "dog" in message.content.lower() and "doggo" not in message.content.lower():
        await message.channel.send(pasta.copypastas.doggoPas, delete_after=20.0)

#--------------------------------------------------------------------------------------------------------------------------
    #autofilter:
    for word in pasta.listsPas.autoMutePas:
      if word in msgContent:
        await message.delete()
        await message.channel.send(f"{message.author.mention} you can't send that!")

  await bot.process_commands(message)

#--------------------------------------------------------------------------------------------------------------------------
## wow nice
#necessities

keep_alive()
bot.run(my_secret)