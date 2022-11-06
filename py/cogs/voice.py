import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
from asyncio import sleep


class Voice(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._last_member = None
        
        
    @app_commands.command(
        name="play_sound",
        description="Plays a sound in vc",
    )
    async def mlg(self, inter: discord.Interaction) -> None:
        vClient: discord.VoiceClient = get(self.bot.voice_clients, guild=inter.guild)
        file = discord.FFmpegPCMAudio("mlg.mp3")
        vClient.play(file, after=None)
            
        
        
        
        
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Voice(bot))