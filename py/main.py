import os
import time

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import speech_recognition as sr


from pasta import file_to_dict, file_to_list, sec2days, ogg2wav, DATA

# loading in environmental variables
load_dotenv()
TOKEN: str = os.environ.get("TOKEN")
WH_URL: str = os.environ.get("url")


# initialising the bot
intents: discord.Intents = discord.Intents.all()
bot: commands.Bot = commands.Bot(
    command_prefix=".",
    intents=intents,
)

initial_extensions: list[str] = [
    "cogs.admin",           # admin commands
    "cogs.porl",            # porl commands
    # "cogs.hive",            # hive commands # they changed the api a bunch 
    "cogs.everyone",        # everyone commands
    "cogs.mod",             # mod commands
    # "cogs.voice",           # voice commands
    "cogs.latex",           # latex commands
]

async def load_cogs(exts: list[str]) -> None:
    """ Load in commands from other files """
    for ext in exts:
        await bot.load_extension(ext)

#--------------------------------------------------------------------------------------------------------------------------
# loading data in from files


data = DATA

channels: dict = file_to_dict(data + "channels.json")
roles: dict = file_to_dict(data + "roles.json")
jojo: dict = file_to_dict(data + "jojo.json")
copypastas: dict = file_to_dict(data + "copypastas.json")

censor: list = file_to_list(data + "censor.txt")

#--------------------------------------------------------------------------------------------------------------------------

@bot.listen()
async def on_ready() -> None:
    """ When the bot is first started, runs once """

    print(f"Logged on as {bot.user}")

    # loading in the commands that are kept in other files
    try:
        await load_cogs(initial_extensions)
    except Exception as e:
        print(f"{e}")

    await bot.tree.sync()
    print("Commands successfully synced and loaded.")

    # jojolands update
    if not loop.is_running():
        loop.start()



#--------------------------------------------------------------------------------------------------------------------------

@bot.listen()
async def on_member_join(member: discord.Member) -> None:
    """ When a member joins. """

    guild: discord.Guild = member.guild

    if member.bot: # cant dm bots/dont add the wrong roles to them
        bot_role = discord.utils.get(guild.roles, id=roles["bot"])
        await member.add_roles(bot_role)
        return

    # welcome message
    general: discord.TextChannel = guild.get_channel(channels["general"])

    await general.send(f"Welcome {member.mention}, hope you have a good time in the server!")

    # giving member role
    for roleID in roles["onJoin"]:
        role: discord.Role = discord.utils.get(guild.roles, id=roleID)
        await member.add_roles(role)
    

#--------------------------------------------------------------------------------------------------------------------------

@bot.listen()
async def on_member_remove(member: discord.Member) -> None:
    if member.bot: return
    
    gen: discord.TextChannel = bot.get_channel(channels["general"])
    await gen.send(f"{member.mention} has left the server.........")

#--------------------------------------------------------------------------------------------------------------------------


async def transcribe_message(msg: discord.Message) -> str:
    """ Transcribes a discord voice message to text using google ai API """
    
    # placeholder message
    reply = await msg.reply("working....", mention_author=False)
    #  save the .ogg file locally and convert it to a .wav locally
    fname: str = f"{msg.id}.ogg"
    await msg.attachments[0].save(f"{fname}")
    ogg2wav(fname)
    
    # no idea 
    r: sr.Recognizer = sr.Recognizer()
    v_msg: sr.AudioFile = sr.AudioFile(f"{msg.id}.wav")
    with v_msg as src: audio = r.record(src)
    
    # delete the files after theyre downloaded to stop them from taking up space
    os.remove(f"{fname}")
    os.remove(f"{msg.id}.wav")
    
    # respond to the message with the transcribed text
    try:
        await reply.edit(content=f"```{str(r.recognize_google(audio))}```")
    except sr.exceptions.UnknownValueError: # if any sound cannot be recognised by the ai
        await reply.edit(content="```I am super homophobic.```")
    

@bot.listen()
async def on_message(msg: discord.Message) -> None:
    if msg.author.bot:
        return

    # i lowkey dk
    transcribe_everything: bool = True
    if transcribe_everything and msg.flags.value >> 13 and len(msg.attachments) == 1:
        await transcribe_message(msg)


    # AUTOREPLY (copypastas)
    msgC: str = msg.content.lower()

    if "vaporeon" in msgC: 
        await msg.channel.send(copypastas["vaporeon"], delete_after=20.0)
    
    if "gaming laptop" in msgC:
        await msg.channel.send(copypastas["laptop"], delete_after=20.0)
    
    if "meow" in msgC:
        await msg.channel.send(copypastas["meow"], delete_after=20.0)
    
    if "downvote" in msgC:
        await msg.channel.send(copypastas["downvote"], delete_after=20.0)
    
    if "dog" in msgC and "doggo" not in msgC:
        await msg.channel.send(copypastas["doggo"], delete_after=20.0)


    # autofilter:
    
    for word in censor:
        if word in msgC:
            muteID: int = roles["muted"]
            mute: discord.Role = msg.guild.get_role(muteID)

            await msg.author.add_roles(mute)
            await msg.delete()
            await msg.channel.send(f"{msg.author.mention} you can't send that!")
        

    # AUTOREACTS

    if (msg.channel.id is channels["suggestions"]) or ("y/n" in msgC):
        up: str = '\N{THUMBS UP SIGN}'
        down: str = '\N{THUMBS DOWN SIGN}'
        await msg.add_reaction(up)
        await msg.add_reaction(down)
        
        
#--------------------------------------------------------------------------------------------------------------------------
# loop for fun stuff (like a countdown)


@tasks.loop(seconds=4)
async def loop() -> None:
    """ Countdown to the next jojolands chapter """
    jojo = file_to_dict(data + "jojo.json")
    # if not jojo_pinged:
    alarm: int = jojo["timestamp"]
    time_now: float = time.time()
    diff: int = round(alarm - time_now)
    
    # To make it count on each minute rather than a few seconds off
    if diff % 4 != 0:
        time.sleep((diff % 4))
    
    if diff < 0:
        # jojo_pinged = True
        await bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Game(name=f"{jojo['event']} is here!")
        )
        
        # general = bot.get_channel(
        #     ChannelIDs.gen
        # )
        
        # porl = bot.get_user(
        #     pasta.UserIDs.porlUserID
        # )
        
        # await general.send(
        #     f"JOJOLands ch. {pasta.nextChap} is here! {porl.mention}"
        # )
        
    else:
        await bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Game(name=f"{sec2days(diff)} until {jojo['event']}!")
        )
        

bot.run(TOKEN)