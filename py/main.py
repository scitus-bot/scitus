import discord
from discord.ext import commands
from discord.utils import get
import pasta
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.environ.get('TOKEN')

#print(datetime.today().weekday())
#monday = 0, sunday = 6

# shoutout u/Bals2008 for being extremely swaggy


# 7.5.22 decided to run the bot from my laptop rather than repl

# (22.7.22) Beginning to migrate to slash commands 
# This is probably going to take a while (hopefully the whole summer holidays)

#--------------------------------------------------------------------------------------------------------------------------
#weird stuff i dont get
#token is unique, cant give that to you

#weird stuff
prefix = pasta.prefixPasta #change prefix in pasta.py
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    intents=intents, 
    command_prefix=prefix, 
    case_insensitive=True,
    )

# github webhook test part 2

@bot.listen()
async def on_ready():
    print(f"Logged on as: {bot.user}")
    
    gen = bot.get_channel(pasta.ChannelIDs.gen)
    await gen.send("The bot is now online!")
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="peace and love 😎✌️🌟❤️🎶🌈☮️",
            )
        )


#--------------------------------------------------------------------------------------------------------------------------
# loading in each cog

initial_extensions = [
    "cogs.everyone",        # everyone commands
    "cogs.mod",             # mod commands
    "cogs.porl",            # porl commands
    "cogs.admin",           # admin commands
    "cogs.hive",            # hive commands
    ]

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


#--------------------------------------------------------------------------------------------------------------------------
# on_user_join 

@bot.listen()
async def on_member_join(member: discord.Member):

    # welcome message

    guild = member.guild
    
    
    general = guild.get_channel(pasta.ChannelIDs.gen)
    ruleID = pasta.ChannelIDs.rules
    
    await general.send(f"Welcome {member.mention}, hope you have a good time in the server! Check out <#{ruleID}> for the rules!")
    
    if member.bot: # dont want the hassle of dming bots and assigning roles and etc
        botRole = get(guild.roles, id=709182248213020705)
        await member.add_roles(botRole)
        return
    
    
#--------------------------------------------------------------------------------------------------------------------------
    # give roles

    for roleID in pasta.JoinRoleIDs.giveRoleIDS:
        role = get(guild.roles, id=roleID)
        await member.add_roles(role)
    
    
#--------------------------------------------------------------------------------------------------------------------------
    # silly little image

    await member.send("https://images-ext-1.discordapp.net/external/AQAbFMaLzdhzzS8lX2tGQ-5mejo6KqycKl8Z5tK-BFU/https/media.discordapp.net/attachments/709182248741503093/905499003754541116/c9de64f4432ebbc2fde22a968dbff7dd.png")


#--------------------------------------------------------------------------------------------------------------------------
# on leave

@bot.listen()
async def on_member_remove(member: discord.Member):
    
    gen = bot.get_channel(pasta.ChannelIDs.gen)
    await gen.send(f"{member.mention} has left the server..... what a loser")


#--------------------------------------------------------------------------------------------------------------------------
#on_message

@bot.listen()
async def on_message(msg: discord.Message):
    if msg.author.bot:
        return
    
    msgContent = msg.content.lower()

    # print(type(msg)) # discord.message.Message
    #if i get pinged, it will tell them to shut up # (removed)
    
    mentioned = msg.mentions
    for user in mentioned:
        if user.id == 848209731474817094: #bot
            porl = bot.get_user(409821972026097667)
            await porl.send(f"{msgContent} - sent by - {msg.author.mention}")


#--------------------------------------------------------------------------------------------------------------------------
    #AUTOREPLY (copypastas)
    #finding how to do case insensitive things 

    if "vaporeon" in msgContent: #Green squigglies show up but you can ignore them.
        await msg.channel.send(pasta.CopyPastas.vaporeonPas, delete_after=20.0)
    
    if "gaming laptop" in msgContent:
        await msg.channel.send(pasta.CopyPastas.laptopPas, delete_after=20.0)
    
    if "meow" in msgContent:
        await msg.channel.send(pasta.CopyPastas.meowPas, delete_after=20.0)
    
    if "downvote" in msgContent:
        await msg.channel.send(pasta.CopyPastas.downfaqPas, delete_after=20.0)
    
    if "dog" in msgContent and "doggo" not in msgContent:
        await msg.channel.send(pasta.CopyPastas.doggoPas, delete_after=20.0)


#-------------------------------------------------------------------------------------------------------------------------
    #autofilter:
    
    # trolling
    if "genshin" in msgContent or "impact" in msgContent or "america" in msgContent or "jesus" in msgContent or "oh" in msgContent:
        await msg.delete()
    
    for word in pasta.ListsPas.autoMutePas:
        if word in msgContent:
            member = msg.author
            muteID = pasta.RoleIDs.mutedRoleID
            mute = msg.guild.get_role(muteID)

            await member.add_roles(mute)
            await msg.delete()
            await msg.channel.send(f"{msg.author.mention} you can't send that!")
        

#--------------------------------------------------------------------------------------------------------------------------
    #AUTOREACTS

    if ("y/n" in msgContent):
        up = '\N{THUMBS UP SIGN}'
        down = '\N{THUMBS DOWN SIGN}'
        await msg.add_reaction(up)
        await msg.add_reaction(down)
        

#--------------------------------------------------------------------------------------------------------------------------

## wow nice
#necessities

bot.run(BOT_TOKEN)
