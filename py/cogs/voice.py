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
        # discord.opus.load_opus("opus")
        channel = inter.user.voice.channel
        
        if channel:
            voice = await channel.connect()
            voice.play(discord.FFmpegPCMAudio("mlg.mp3"))
            await inter.response.send_message("playing sound")
            await sleep(10)
            await voice.disconnect()
            
            

        
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Voice(bot))