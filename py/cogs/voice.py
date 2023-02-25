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
        name="join-voice",
        description="joins the vc the user is in",
    )
    async def join(self, inter: discord.Interaction) -> None:
        # shit does not want to work lmaoo
        # discord.opus.load_opus("opus")
        channel = inter.user.voice.voice_channel
        
        if channel:
            voice = await channel.connect()
            
    @app_commands.command(
        name="leave-voice",
        description="leaves the current voice channel",
    )
    async def join(self, inter: discord.Interaction) -> None:
        if self.bot.voice.voice_channel:
            pass
            
            

        
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Voice(bot))