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
bot = commands.Bot(intents=intents, command_prefix=prefix, case_insensitive=True)

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
  
  
  #if i get pinged, it will tell them to shut up
  mentioned = message.mentions
  for user in mentioned:
    if message.author.id == 848209731474817094:#bot
      return

    #elif user.id == 409821972026097667: #me
    #  await message.channel.send("kindly shut up")
    
    elif user.id == 848209731474817094: #bot
      porl = bot.get_user(409821972026097667)
      await porl.send(str(message.content) + "  -  sent by " + str(message.author))

  #next

#--------------------------------------------------------------------------------------------------------------------------

  #AUTOREPLY (copypastas)
  #finding how to do case insensitive things 
  if message.author.id == 848209731474817094: #scitus id
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
        if word in message.content:
            role = get(message.author.guild.roles, id=pasta.roleIDS.mutedRoleID)
            await message.author.add_roles(role)
            await message.channel.send(f"bad language {message.author.mention}")
            await message.delete()

#--------------------------------------------------------------------------------------------------------------------------
  #I have "coder's block" :(  
  await bot.process_commands(message)

@bot.event
async def on_member_join(member):
  await member.send("https://media.discordapp.net/attachments/709182248741503093/905499003754541116/c9de64f4432ebbc2fde22a968dbff7dd.png")
  await bot.process_commands(member)

  async for role in pasta.joinRoleIDs:
    member.add_roles(get(member.guild.roles, id=role))

#end of command





#--------------------------------------------------------------------------------------------------------------------------
## wow nice
#necessities

keep_alive()
bot.run(my_secret)