#This is a file that contains copypastas/user IDs/role IDs
import discord
import json
from pdf2image import convert_from_path
from pydub import AudioSegment

# cwd = r"C:\Users\nathan\code\discord\scitus\py" + "\\"
# AudioSegment.converter = r"C:\Users\nathan\code\ffmpeg\ffmpeg.exe"

DATA = r"data\\"

def success_embed(desc: str = None) -> discord.Embed:
    """ Generates a basic embed for successful processes. """
    embed: discord.Embed = discord.Embed(
        title="Success",
        colour=discord.Colour.green(),
        description=desc,
    )
    return embed

def fail_embed(desc: str = None) -> discord.Embed:
    """ Generates a basic embed for failed processes. """
    embed: discord.Embed = discord.Embed(
        title="Failure",
        colour=discord.Colour.red(),
        description=desc,
    )
    return embed

#--------------------------------------------------------------------------------------------------------------------------

def file_to_dict(filename: str) -> dict:
    """ Returns a dictionary from a JSON file """
    
    if filename[-5:].lower() != ".json":
        raise ValueError("Not a JSON file")
    
    with open(filename, "r") as file:
        return json.load(file)


def file_to_list(filename: str) -> list:
    """ Returns the lines in the file """

    with open(filename, "r") as file:
        return [l.strip() for l in file.readlines()]
    
    
def pdf_to_image(file_name: str) -> None:
    pages: list = convert_from_path(file_name, 500)
    for count, page in enumerate(pages):
        page.save(f"{count}.jpg", "JPEG")
        
        
def sec2days(sec: int) -> str:
    """ Converts an amount of seconds into a nice string """
    mns: int = (sec) // 60
    hrs: int = (mns) // 60
    day: int = (hrs) // 24
    mns -= hrs*60
    hrs -= day*24
    ret_str: str = ""
    
    days = f"{day} day(s), " if day != 0 else ""
    hrss = f"{hrs} hour(s), " if hrs != 0 else ""
    mnss = f"{mns} minute(s), and " if mns != 0 else ""

    ret_str = days + hrss + mnss + f"{sec%60} second(s)"

    return ret_str


def ogg2wav(fname: str) -> None:
    """ Converts an .ogg to a .wav file"""
    # fname = cwd + fname
    wfn = fname.replace(".ogg",".wav")
    # print(fname)
    x = AudioSegment.from_file(fname)
    x.export(wfn, format="wav")