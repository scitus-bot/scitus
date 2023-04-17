from pasta import ChannelIDs, ListsPas, JoinRoleIDs, CopyPastas, RoleIDs, prefixPasta
import pasta
from discord.ext import commands, tasks
from discord import app_commands
import speech_recognition as sr
from dotenv import load_dotenv
from pydub import AudioSegment
import discord
import os
import requests as r
import time

load_dotenv()
TOKEN: str = os.environ.get("TOKEN")
WH_URL: str = os.environ.get("url")

intents: discord.Intents = discord.Intents.all()
bot: commands.Bot = commands.Bot(
    command_prefix=prefixPasta,
    intents=intents,
)


initial_extensions: list[str] = [
    "cogs.admin",           # admin commands
    "cogs.porl",            # porl commands
    "cogs.hive",            # hive commands
    "cogs.everyone",        # everyone commands
    "cogs.mod",             # mod commands
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
    
    # loading in the commands that are kept in other files
    try:
        await load_cogs(initial_extensions)
    except Exception as e:
        print(f"{e}")
    
    await bot.tree.sync()
    
    print("Commands successfully synced and loaded.")
    
    if not loop.is_running():
        loop.start()



#--------------------------------------------------------------------------------------------------------------------------

@bot.listen()
async def on_member_join(member: discord.Member) -> None:

    # welcome message
    
    guild: discord.Guild = member.guild
    general: discord.TextChannel = guild.get_channel(ChannelIDs.gen)
    ruleID: int = ChannelIDs.rules
    
    await general.send(f"Welcome {member.mention}, hope you have a good time in the server!")
    
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

def ogg2wav(fname: str) -> None:
    wfn = fname.replace('.ogg','.wav')
    x = AudioSegment.from_file(f"scitus/py/{fname}")
    x.export(f"scitus/py/{wfn}", format='wav')    # maybe use original resolution to make smaller


async def transcribe_message(msg: discord.Message) -> str:
    reply = await msg.reply("working hard", mention_author=False)
    fname: str = f"{msg.id}.ogg"
    await msg.attachments[0].save(f"scitus/py/{fname}")
    ogg2wav(fname)
    
    r: sr.Recognizer = sr.Recognizer()
    v_msg: sr.AudioFile = sr.AudioFile(f"scitus/py/{msg.id}.wav")
    
    with v_msg as src:
        audio = r.record(src)
        
    os.remove(f"scitus/py/{fname}")
    os.remove(f"scitus/py/{msg.id}.wav")
    
    try:
        await reply.edit(content=f"```{str(r.recognize_google(audio))}```")
    except sr.exceptions.UnknownValueError:
        await reply.edit(content="```I am super homophobic and racist.```")
    
    

#--------------------------------------------------------------------------------------------------------------------------

@bot.listen()
async def on_message(msg: discord.Message) -> None:
    if msg.author.bot: return
    
    msgC: str = msg.content.lower()
    
    # "message.flags.value >> 13" should be replacable with "message.flags.voice" when VM support comes to discord.py, I think.
    transcribe_everything: bool = True
    if transcribe_everything and msg.flags.value >> 13 and len(msg.attachments) == 1:
        await transcribe_message(msg)
#--------------------------------------------------------------------------------------------------------------------------
    # AUTOREPLY (copypastas)
    # finding how to do case insensitive things 

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
    # autofilter:
    
    for word in ListsPas.autoMutePas:
        if word in msgC:
            muteID: int = RoleIDs.mutedRoleID
            mute: discord.Role = msg.guild.get_role(muteID)

            await msg.author.add_roles(mute)
            await msg.delete()
            await msg.channel.send(f"{msg.author.mention} you can't send that!")
        

#--------------------------------------------------------------------------------------------------------------------------
    # AUTOREACTS

    if (msg.channel.id is ChannelIDs.suggestions) or ("y/n" in msgC):
        up: str = '\N{THUMBS UP SIGN}'
        down: str = '\N{THUMBS DOWN SIGN}'
        await msg.add_reaction(up)
        await msg.add_reaction(down)
        
        
#--------------------------------------------------------------------------------------------------------------------------

def sec2days(sec: int) -> str:
    min: int = (sec) // 60
    hrs: int = (min) // 60
    day: int = (hrs) // 24
    min -= hrs*60
    hrs -= day*24
    ret_str: str = ""
    
    ret_str = f"{day} day(s), {hrs} hour(s), {min} minute(s)"
    
    return ret_str

@tasks.loop(minutes=1)
async def loop() -> None:
    alarm: int = pasta.nextJoJo
    time_now: float = time.time()
    diff: int = round(alarm - time_now)
    
    if diff < 60:
        await bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Game(name=f"JOJOLands ch. {pasta.nextChap} is here!")
        )
    else:
        await bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Game(name=f"{sec2days(diff)} until JOJOLands ch. {pasta.nextChap}!")
        )
        
    
    


bot.run(TOKEN)