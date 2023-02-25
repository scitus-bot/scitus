# attempting to rewrite scitus using the new discord.py 2.0 along with slash commands
import discord
from discord import app_commands
from discord.ext import commands
from pasta import ChannelIDs, ListsPas, JoinRoleIDs, CopyPastas, RoleIDs, prefixPasta
import os
from dotenv import load_dotenv
import requests as r
load_dotenv()
TOKEN: str = os.environ.get("TOKEN")
WH_URL: str = os.environ.get("url")

intents: discord.Intents = discord.Intents.all()
# client: discord.Client = discord.Client(intents=intents)
bot: commands.Bot = commands.Bot(
    command_prefix=prefixPasta,
    intents=intents,
)


initial_extensions: list[str] = [
    "cogs.everyone",        # everyone commands
    "cogs.mod",             # mod commands
    "cogs.porl",            # porl commands
    "cogs.admin",           # admin commands
    "cogs.hive",            # hive commands
    "cogs.voice",           # voice commands
]

async def load_cogs(exts: list[str]) -> None:
    for ext in exts:
        await bot.load_extension(ext)



""" 
To Do:
    Message filter
    On join + leave
    On message silly things
        jesus -> allah
        
"""



#--------------------------------------------------------------------------------------------------------------------------

@bot.listen()
async def on_ready() -> None:
    print(f"Logged on as {bot.user}")
    
    # changing the status of the client
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="peace and love 😎✌️🌟❤️🎶🌈☮️",
            )
    )
    
    # loading in the commands that are kept in other files
    await load_cogs(initial_extensions)
    
    await bot.tree.sync()
    
    print("Commands successfully synced and loaded.")


#--------------------------------------------------------------------------------------------------------------------------

@bot.listen()
async def on_member_join(member: discord.Member) -> None:

    # welcome message
    
    guild: discord.Guild = member.guild
    general: discord.TextChannel = guild.get_channel(ChannelIDs.gen)
    ruleID: int = ChannelIDs.rules
    
    await general.send(f"Welcome {member.mention}, hope you have a good time in the server! Check out <#{ruleID}> for the rules!")
    
    if member.bot: # dont want the hassle of dming bots and assigning roles and etc
        botRole = discord.utils.get(guild.roles, id=709182248213020705)
        await member.add_roles(botRole)
        return
    
    
#--------------------------------------------------------------------------------------------------------------------------
    # give roles

    for roleID in JoinRoleIDs.giveRoleIDS:
        role: discord.Role = discord.utils.get(guild.roles, id=roleID)
        await member.add_roles(role)
    
    
#--------------------------------------------------------------------------------------------------------------------------
    # silly little image

    await member.send("https://images-ext-1.discordapp.net/external/AQAbFMaLzdhzzS8lX2tGQ-5mejo6KqycKl8Z5tK-BFU/https/media.discordapp.net/attachments/709182248741503093/905499003754541116/c9de64f4432ebbc2fde22a968dbff7dd.png")


#--------------------------------------------------------------------------------------------------------------------------

@bot.listen()
async def on_member_remove(member: discord.Member) -> None:
    if member.bot: return
    
    gen: discord.TextChannel = bot.get_channel(ChannelIDs.gen)
    await gen.send(f"{member.mention} has left the server.........")


#--------------------------------------------------------------------------------------------------------------------------

@bot.listen()
async def on_message(msg: discord.Message) -> None:
    if msg.author.bot: return
    
    msgC: str = msg.content.lower()
    
    
#--------------------------------------------------------------------------------------------------------------------------
    #AUTOREPLY (copypastas)
    #finding how to do case insensitive things 

    if "vaporeon" in msgC: 
        await msg.channel.send(CopyPastas.vaporeonPas, delete_after=20.0)
    
    if "gaming laptop" in msgC:
        await msg.channel.send(CopyPastas.laptopPas, delete_after=20.0)
    
    if "meow" in msgC:
        await msg.channel.send(CopyPastas.meowPas, delete_after=20.0)
    
    if "downvote" in msgC:
        await msg.channel.send(CopyPastas.downfaqPas, delete_after=20.0)
    
    if "dog" in msgC and "doggo" not in msgC:
        await msg.channel.send(CopyPastas.doggoPas, delete_after=20.0)


#-------------------------------------------------------------------------------------------------------------------------
    #autofilter:
    
    for word in ListsPas.autoMutePas:
        if word in msgC:
            muteID: int = RoleIDs.mutedRoleID
            mute: discord.Role = msg.guild.get_role(muteID)

            await msg.author.add_roles(mute)
            await msg.delete()
            await msg.channel.send(f"{msg.author.mention} you can't send that!")
        

#--------------------------------------------------------------------------------------------------------------------------
    #AUTOREACTS

    if (msg.channel.id is ChannelIDs.suggestions) or ("y/n" in msgC):
        up: str = '\N{THUMBS UP SIGN}'
        down: str = '\N{THUMBS DOWN SIGN}'
        await msg.add_reaction(up)
        await msg.add_reaction(down)
        

#--------------------------------------------------------------------------------------------------------------------------
# praise allah

# if jesus is in a message then copy the message text but replace jesus with allah and then post the message using a webhook
# copying the original users pfp and username

    if "jesus" in msgC or "hesus" in msgC:
        await msg.delete()
        # need to put this url into a .env soonr 
        url: str = WH_URL
        quran: str = msgC.replace("jesus", "Allah")
        quran: str = quran.replace("hesus", "Allah")

        data: dict = {
            "content": quran,
            "username": str(msg.author.name),
            "avatar_url": str(msg.author.display_avatar.url),
        }

        result: r.Response = r.post(url, json=data)
        try:
            result.raise_for_status()
        except r.exceptions.HTTPError as err:
            print(err)





bot.run(TOKEN)